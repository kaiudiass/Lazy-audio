import wave
import pyaudio

from config import ARQUIVO_AUDIO


def listar_microfones() -> dict[str, int]:
    microfones = {}
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    for i in range(info.get("deviceCount")):
        dev = p.get_device_info_by_host_api_device_index(0, i)
        if dev.get("maxInputChannels") > 0:
            microfones[dev.get("name")] = i
    p.terminate()
    return microfones


def gravar(indice_dispositivo: int, tecla_fn, on_inicio=None, on_fim=None) -> bool:
    CHUNK   = 1024
    FORMATO = pyaudio.paInt16
    CANAIS  = 1
    TAXA    = 44100

    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=FORMATO, channels=CANAIS, rate=TAXA,
            input=True, frames_per_buffer=CHUNK,
            input_device_index=indice_dispositivo,
        )
    except Exception:
        p.terminate()
        return False

    if on_inicio:
        on_inicio()

    frames = []
    while tecla_fn():
        frames.append(stream.read(CHUNK))

    stream.stop_stream()
    stream.close()
    p.terminate()

    if on_fim:
        on_fim()

    if not frames:
        return False

    wf = wave.open(ARQUIVO_AUDIO, "wb")
    wf.setnchannels(CANAIS)
    wf.setsampwidth(p.get_sample_size(FORMATO))
    wf.setframerate(TAXA)
    wf.writeframes(b"".join(frames))
    wf.close()
    return True
