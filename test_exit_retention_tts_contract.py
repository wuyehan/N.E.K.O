from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def read_repo_file(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_exit_retention_tts_uses_current_character_voice_with_bounded_text():
    router = read_repo_file("main_routers/characters_router.py")

    assert "@router.post('/exit_retention_tts')" in router
    assert "async def synthesize_exit_retention_tts" in router
    assert "characters.get('当前猫娘'" in router
    assert "get_reserved(\n        current_catgirl_payload,\n        'voice_id'," in router
    assert "await _resolve_exit_retention_voice_id(" in router
    assert "EXIT_RETENTION_TTS_TEXT_MAX_CHARS" in router
    assert "text[:EXIT_RETENTION_TTS_TEXT_MAX_CHARS]" in router
    assert "return await get_voice_preview(" in router
    assert "text=text" in router


def test_exit_retention_tts_falls_back_to_current_tts_route_when_character_voice_is_empty():
    router = read_repo_file("main_routers/characters_router.py")

    assert "async def _resolve_exit_retention_voice_id(" in router
    assert "core_config = await config_manager.aget_core_config()" in router
    assert "core_config.get('TTS_VOICE_ID')" in router
    assert "core_config.get('CORE_API_TYPE')" in router
    assert "get_stepfun_tts_default_voice" in router
    assert '"Momo"' in router
    assert "CURRENT_CATGIRL_VOICE_MISSING" not in router


def test_exit_retention_tts_applies_sad_reluctant_voice_style_to_supported_providers():
    router = read_repo_file("main_routers/characters_router.py")
    voice_clone = read_repo_file("utils/voice_clone.py")

    assert 'EXIT_RETENTION_TTS_STYLE = "sad_reluctant"' in router
    assert "voice_style=EXIT_RETENTION_TTS_STYLE" in router
    assert "voice_style: str | None = None" in router

    assert "EXIT_RETENTION_TTS_GEMINI_STYLE_INSTRUCTION" in router
    assert "style_instruction=style_instruction" in router

    assert "EXIT_RETENTION_TTS_ELEVENLABS_STYLE" in router
    assert '"style": style' in router

    assert "EXIT_RETENTION_TTS_PROVIDER_EMOTION" in router
    assert 'create_data["emotion"] = emotion' in router
    assert 'voice_setting["emotion"] = emotion' in voice_clone
    assert "emotion=provider_emotion" in router


def test_voice_preview_accepts_explicit_text_for_non_preview_callers():
    router = read_repo_file("main_routers/characters_router.py")

    assert "async def get_voice_preview(" in router
    assert "text: str | None = None" in router
    assert "explicit_text = str(text or '').strip()" in router
    assert "preview_line = explicit_text or _loc(VOICE_PREVIEW_TEXTS, preview_language)" in router


if __name__ == "__main__":
    test_exit_retention_tts_uses_current_character_voice_with_bounded_text()
    test_exit_retention_tts_falls_back_to_current_tts_route_when_character_voice_is_empty()
    test_exit_retention_tts_applies_sad_reluctant_voice_style_to_supported_providers()
    test_voice_preview_accepts_explicit_text_for_non_preview_callers()
