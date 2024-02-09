##leavcing this one here as an example of my bad code


from saucenao_api import SauceNao 
import os, random, requests,time,sys
# Replace the key with your own
Source_folder = "E:\\Weeb posting\\#sort batch\\New Sample\\" # Where to pull when saving
Renamed = "E:\\Weeb posting\\#sort batch\\Boorued\\" # where to move
No_Booru = "E:\\Weeb posting\\#sort batch\\NoBooru\\" # where to move 

count = 0 # its a 
# Iterate directory
for path in os.listdir(Source_folder):
    # check if current path is a file
    if os.path.isfile(os.path.join(Source_folder, path)):
        count += 1
print("items to scan")        
print(count)

      
sauce = SauceNao('xxxx')
for _ in range(count): # amount to sort
  Randfile = random.choice(os.listdir(Source_folder))
  f = open(Source_folder + Randfile , 'rb')
  print("File Sent - " + Randfile) 
  results = sauce.from_file(f) 
  f.close() 
  File_addon = ""
  for result in results:
    for url in result.urls:
      print(result.urls)
      print(result.similarity)
      if "https://danbooru.donmai.us/" in url and result.similarity > 85:
        print("we got a match in " + Randfile)
        #Getting Tags
        url1 = url
        Link = url1.replace("/post/show/", "/posts/")
        print(Link)
        r = requests.get(Link+".json")
        j = r.json()
        File_addon = j["tag_string_character"]
        #File_addon = j["tag_string_copyright"]
        print("tags - "+File_addon)
        # Give file to danboru and save result to "File_addon"
        break #we found it
    if File_addon !="":
      break#leaves the loop
  if File_addon !="":
    print("renaming File and moving")
    File_addon = File_addon.replace("/", "")
    File_addon = File_addon.replace(":", "")
    File_addon = File_addon.replace("*", "")
    File_addon = File_addon.replace("?", "")
    File_addon = File_addon.replace('"', '')
    File_addon = File_addon.replace("<", "")
    File_addon = File_addon.replace(">", "")
    File_addon = File_addon.replace("|", "")
    os.replace(Source_folder+Randfile, Renamed+File_addon+"_"+Randfile)
    print("-----")
    time.sleep(1)
  else:
   print("no matches")
   os.replace(Source_folder+Randfile, No_Booru+Randfile)
   print("-----")
   time.sleep(1)
print("Finished")
  



