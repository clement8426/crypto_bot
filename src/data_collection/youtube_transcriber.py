import sys
import os
import subprocess
from faster_whisper import WhisperModel

def download_audio(youtube_url, output_file="audio.mp3"):
    """
    Télécharge l'audio d'une vidéo YouTube
    
    Args:
        youtube_url (str): URL de la vidéo YouTube
        output_file (str): Nom du fichier de sortie
        
    Returns:
        str: Chemin du fichier audio téléchargé
    """
    command = f'yt-dlp -f bestaudio -x --audio-format mp3 -o "{output_file}" "{youtube_url}"'
    subprocess.run(command, shell=True, check=True)
    return output_file

def transcribe_audio(audio_file):
    """
    Transcrit un fichier audio en texte
    
    Args:
        audio_file (str): Chemin du fichier audio
        
    Returns:
        str: Texte transcrit
    """
    model = WhisperModel("base", compute_type="int8")
    segments, info = model.transcribe(audio_file, beam_size=5)
    
    full_text = ""
    for segment in segments:
        full_text += segment.text + " "
    
    return full_text

def save_transcript(transcript, output_file="transcript.txt"):
    """
    Sauvegarde la transcription dans un fichier
    
    Args:
        transcript (str): Texte transcrit
        output_file (str): Nom du fichier de sortie
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print(f"Transcription sauvegardée dans {output_file}")

def main():
    """
    Fonction principale
    """
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcriber.py <youtube_url> [output_file]")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    audio_file = download_audio(youtube_url)
    
    try:
        transcript = transcribe_audio(audio_file)
        
        # Sauvegarder la transcription si un nom de fichier est fourni
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
            save_transcript(transcript, output_file)
        else:
            # Sinon, afficher la transcription
            print(transcript)
    finally:
        # Nettoyage
        if os.path.exists(audio_file):
            os.remove(audio_file)

if __name__ == "__main__":
    main()
