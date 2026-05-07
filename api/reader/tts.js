const { allowCors, fail } = require("../../lib/api/http");
const { parseJsonBody, getClientIp } = require("../../lib/api/request");
const { takeRateLimitToken } = require("../../lib/api/rate-limit");

const CAMB_BASE_URL = "https://client.camb.ai/apis";
const DEFAULT_CAMB_VOICE_ID = 147320;
const MAX_TTS_CHARS = 3000;
let cachedVoice = null;

async function findCambVoiceId(apiKey) {
  const configured = Number(
    process.env.CAMB_KENTA_VOICE_ID || process.env.CAMB_VOICE_ID || "",
  );
  if (Number.isFinite(configured) && configured > 0) {
    return configured;
  }
  if (cachedVoice && Date.now() - cachedVoice.checkedAt < 60 * 60 * 1000) {
    return cachedVoice.id;
  }

  try {
    const response = await fetch(`${CAMB_BASE_URL}/list-voices`, {
      headers: { "x-api-key": apiKey },
    });
    if (!response.ok) throw new Error(`Voice list failed: ${response.status}`);
    const data = await response.json();
    const voices = Array.isArray(data) ? data : data.voices || [];
    const kenta = voices.find((voice) =>
      String(voice.voice_name || "")
        .toLowerCase()
        .includes("kenta hayashi"),
    );
    cachedVoice = {
      id: Number(kenta?.id) || DEFAULT_CAMB_VOICE_ID,
      checkedAt: Date.now(),
    };
    return cachedVoice.id;
  } catch (error) {
    cachedVoice = { id: DEFAULT_CAMB_VOICE_ID, checkedAt: Date.now() };
    return cachedVoice.id;
  }
}

module.exports = async function handleTts(req, res) {
  if (allowCors(req, res)) return;
  if (req.method !== "POST") {
    fail(res, 405, "Method not allowed");
    return;
  }
  if (!takeRateLimitToken(`tts:${getClientIp(req)}`, 45, 60_000)) {
    fail(res, 429, "Too many narration requests");
    return;
  }

  const apiKey = process.env.CAMB_API_KEY || "";
  if (!apiKey) {
    fail(res, 503, "CAMB_API_KEY is not configured");
    return;
  }

  try {
    const body = await parseJsonBody(req);
    const text = String(body.text || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, MAX_TTS_CHARS);
    if (text.length < 3) {
      fail(res, 400, "Text is too short");
      return;
    }

    const requestedLanguage = String(body.language || "").toLowerCase();
    const language =
      requestedLanguage === "ja" || requestedLanguage === "ja-jp"
        ? "ja-jp"
        : "en-us";
    const model =
      body.model === "mars-pro" || body.model === "mars-instruct"
        ? body.model
        : "mars-flash";
    const voiceId = await findCambVoiceId(apiKey);

    const cambResponse = await fetch(`${CAMB_BASE_URL}/tts-stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
      },
      body: JSON.stringify({
        text,
        language,
        voice_id: voiceId,
        speech_model: model,
        user_instructions:
          model === "mars-instruct"
            ? "Deep, calm, cinematic narration with clear pacing."
            : null,
        enhance_named_entities_pronunciation: true,
        output_configuration: {
          format: "mp3",
          duration: null,
          apply_enhancement: true,
        },
        voice_settings: {
          enhance_reference_audio_quality: false,
          maintain_source_accent: false,
        },
        inference_options: {
          stability: 0.68,
          temperature: 0.7,
          speaker_similarity: 0.75,
        },
      }),
    });

    if (!cambResponse.ok) {
      fail(res, cambResponse.status, "CAMB narration failed");
      return;
    }

    const audio = Buffer.from(await cambResponse.arrayBuffer());
    res.statusCode = 200;
    res.setHeader("Content-Type", "audio/mpeg");
    res.setHeader("Cache-Control", "no-store");
    res.setHeader("X-Threadborn-Voice", String(voiceId));
    res.end(audio);
  } catch (error) {
    fail(res, 500, "Narration unavailable");
  }
};
