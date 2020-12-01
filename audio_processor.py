import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class GetPartTextFromAudio:
	api_key = 'EB72E803F05E421E93E2'
	
	def __init__(self, wav_file_path):
		self.wav_file_path = wav_file_path
		
	def send_request_for_audio_conversion(self):
		multipart_data = MultipartEncoder(
			fields={
					'filePath': ('file.wav', open(self.wav_file_path, 'rb')),
					'samplerate': '16000', 
					'channel': '1',
					'normalize': 'yes'
				   }
			)

		response = requests.post('https://apis.sentient.io/microservices/utility/audioprocessing/v0.1/getresults', 
								 data=multipart_data, 
								 headers={
									 'Content-Type': multipart_data.content_type,
									 'x-api-key': self.api_key
								 })
		return response.json()


	def send_request_for_speech_to_text_conversion(self, binary_wav_string):
		payload = {
			'model': 'news_parliament',
			'wav_base64': binary_wav_string                                
		}
		payload_json = json.dumps(payload)
		response = requests.post('https://apis.sentient.io/microservices/voice/asr/v0.1/getpredictions', 
								 data=payload_json, 
								 headers={
									 'content-type': 'application/json',
									 'x-api-key': self.api_key
								 })
		return response.json()
	
	def get_text_from_response(self, speech_to_text_response):
		response_text = ""
		for speech_utterance in speech_to_text_response['results']:
			response_text = response_text + speech_utterance['text']
		return response_text   
		
	def process(self):
		audio_conversion_response = self.send_request_for_audio_conversion()
		speech_to_text_response = self.send_request_for_speech_to_text_conversion(audio_conversion_response['results']['AudioContent']) 
		return self.get_text_from_response(speech_to_text_response)


class GetCompleteTextForAudio:
	HOME_PATH = "/home/kartikeysingh/Desktop/Sentinet"
	
	def __init__(self, file_name):
		self.file_name = file_name
		self.RESOURCE_PATH = f"resources/music/{file_name}_outputs/spleeter/"	

	def split_and_remove_noise(self):
		os.system("cd " + self.HOME_PATH + " & ./split_file.sh " + self.file_name)

	def get_all_part_texts(self):
		audio_parts = os.listdir(self.RESOURCE_PATH)
		complete_text = ""	
		for file in audio_parts:
			audio_part = os.path.join(self.RESOURCE_PATH, file) + "/vocals.wav"
			part_text = GetPartTextFromAudio(audio_part).process()
			complete_text = complete_text + " " + part_text
		print(complete_text)
		return complete_text	    	

	def process(self):
		self.split_and_remove_noise()
		return self.get_all_part_texts()

if __name__ == '__main__':
	GetCompleteTextForAudio("20.mp3").get_all_part_texts()