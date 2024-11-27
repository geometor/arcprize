import google.generativeai as genai
import os
import PIL.Image

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash".
#  response = model.generate_content("Write a story about a magic backpack.")
#  print(response.text)

#  organ = PIL.Image.open("/home/phiarchitect/Downloads/arcprize.org_play.png")
#  response = model.generate_content(["describe the image", organ])
#  print(response.text)

#  myfile = genai.upload_file("../refs/ARC-800-tasks/first-six/artifacts/1-3aa6fb7a/train_1/input_32.png")
#  print(f"{myfile=}")

#  result = model.generate_content(
    #  [myfile, "\n\n", "describe the image"]
#  )
#  print(f"{result.text=}")
#  model = genai.GenerativeModel(model_name='gemini-1.5-pro')

response = model.generate_content(
    ('What is the sum of the first 50 prime numbers? '
    'Generate and run code for the calculation.'),
    tools='code_execution')

print(response.text)
