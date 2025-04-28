import speech_recognition as sr
import ffmpeg
import threading
import os

def transcribe_from_mic():
    recognizer = sr.Recognizer()

    print("Adjusting for ambient noise... Please wait.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening for live speech... (Press CTRL+C to stop)")

        try:
            while True:
                audio = recognizer.listen(source)

                try:
                    text = recognizer.recognize_google(audio)
                    print(f"Caption: {text}")

                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand. Try speaking clearly.")

                except sr.RequestError:
                    print("Error: Check your internet connection.")

        except KeyboardInterrupt:
            print("\nStopped live captioning.")

def extract_audio(video_path, audio_path="temp_audio.wav"):
    try:
        ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True, quiet=True)
        print("Audio extracted successfully.")
        return audio_path
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def transcribe_from_video(video_path):
    recognizer = sr.Recognizer()

    audio_path = extract_audio(video_path)
    if not audio_path:
        return

    with sr.AudioFile(audio_path) as source:
        print("Processing audio from video...")
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            print("\n--- Video Captioning ---")
            print(text)

        except sr.UnknownValueError:
            print("Sorry, could not understand the audio from the video.")

        except sr.RequestError:
            print("Error: Check your internet connection.")

    os.remove(audio_path)  # Clean up temporary audio file

def main():
    print("Choose mode:")
    print("1. Live Captioning")
    print("2. Transcribe from Video")

    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        transcribe_from_mic()
    elif choice == '2':
        video_path = input("Enter video file path: ").strip()
        if os.path.isfile(video_path):
            transcribe_from_video(video_path)
        else:
            print("Invalid video path. Please check the file and try again.")
    else:
        print("Invalid choice. Please restart and select a valid option.")

if __name__ == "__main__":
    main()