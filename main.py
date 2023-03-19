import sys
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import os
credential_path = "/home/hoan/Desktop/detect_text_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))




def text_to_wav(voice_name: str, text: str):
    import google.cloud.texttospeech as tts
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
        

def main():
    print("Start bots!")
    # pdfFile = wi(filename = """/home/hoan/Desktop/itto_chap1.pdf""")
    # image = pdfFile.convert('jpeg')

    # imageBlobs = []

    # #for img in image.sequence:
    # img = image.sequence[1]
    # imgPage = wi(image = img)
    # imageBlobs.append(imgPage.make_blob('jpeg'))

    # extract = []
    #path = "/home/hoan/Documents/reader_bots/test.jpg"
    # imgPage.save(filename=path)

    #for imgBlob in imageBlobs:
    # image = Image.open(io.BytesIO(imageBlobs[0]))
    # text = pytesseract.image_to_string(image, lang = 'vie')
    # extract.append(text)

    # print(extract)
    # detect_text(path)
    text_to_wav("en-AU-Neural2-A", "What is the temperature in Sydney?")

if __name__ == "__main__":
    main()