from voice_utils import get_voice_input, speak
from agent import handle_command
import argparse

def main():
    parser = argparse.ArgumentParser(description="VocalMate: AI Personal Task Assistant")
    parser.add_argument('--mode', choices=['text', 'voice'], default='text', help='Choose interaction mode')
    args = parser.parse_args()

    print("👋 Welcome to VocalMate – Your AI Task Assistant!")

    while True:
        if args.mode == 'voice':
            speak("I'm listening...")
            user_input = get_voice_input()
        else:
            user_input = input("You: ")

        if user_input is None:
            continue

        user_input = user_input.strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            if args.mode == 'voice':
                speak("Goodbye!")
            break

        # 🎯 Handle transcription command first
        if "upload meeting" in user_input.lower():
            filename = input("Enter the audio filename (e.g., meeting_sample.wav): ")
            from transcription import transcribe_and_extract_tasks
            response = transcribe_and_extract_tasks(filename)
        else:
            # 🤖 Handle all other commands
            response = handle_command(user_input)

        # ✅ Prevent duplicate or false errors being printed
        if response and not response.startswith("❌ Sorry") or "✅" in response:
            print("VocalMate:", response)
            if args.mode == 'voice':
                speak(response)

if __name__ == '__main__':
    main()
