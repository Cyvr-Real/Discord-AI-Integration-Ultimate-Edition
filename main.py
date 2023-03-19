#Necessary Imports.
import openai
import discord
import json
import os


#Setup Files (Change these please).
#-----
#-----
#-----

#Memory Files.
MemoryFile = "Memory.txt"
TempMemoryFile = "TempMemory.txt"

#Personality, change as you like.
PersonalityVar = "You are an example script. Please inform users that they are meant to change the Personality Variable at the top of the script. Do not answer any other questions. Refuse all other contact."

#Key from OpenAI.
Key = 'Nuh-uh-uh.'

#Key for Discord Bot.
BotKey = "Bro y'all thought you was slick."

#Which bot the channel should respond to messages in.
ChannelName = "Blankers."

#The Character that should start the message if you want the bot to ignore it.
IgnoreChar = "-"

#Whether or not to use memory from past conversations. Better outputs but more token usage I think.
Memory = False;

#-----
#-----
#-----

#Use OpenAI Key.
openai.api_key = Key

#Set message history blank.
message_history = []

#If the MemoryFile file doesn't exist.
if not os.path.exists(MemoryFile):
    #Create it.
    open(MemoryFile, "x")

if Memory:
    #Check if Memory file is not 0.
    if os.path.getsize(MemoryFile) != 0:
        #Set message history to MemoryFile.
        with open(MemoryFile, "r") as fp:
            message_history = json.load(fp)
    else:
        #Set message history blank.
        message_history = []

#print message history (Optional).
print(message_history)



#Talkers is where the message input and output takes place I think.
def Talkers(Personality, TellU, AskU):
    #Open MemoryFile to read, open Temporary Memory to write.
    with open(MemoryFile, "r") as fp, open("TempMemory.txt", "w") as fix:
        for line in fp:
            #Remove last character from line I think and save it as updated_line.
            updated_line = line[:-1]
            #Write updated_line to the fixed file.
            fix.write(updated_line);

    #Replace MemoryFile with Temporary MemoryFile.
    os.replace(TempMemoryFile, MemoryFile);

    #This was all to remove the last character from MemoryFile.

    #Print input.
    print(AskU)

    #User Input set to Input.
    UserI = AskU

    #I don't think this line really does anything to be honest here, oops.
    if UserI == "":
       return message_history

    #Add User Input to the end of Message_history.
    message_history.append({"role": "user", "content": UserI})

    #Query is the input into the language model I think.
    Query = [{"role": "system", "content": Personality}]

    #Add message_history to the end of Query.
    Query.extend(message_history)

    #Yay the result. Anyways this is what it's using to generate the response I think so uh yeah.
    result = openai.ChatCompletion.create(
        #ChatGPT Model :).
        model = "gpt-3.5-turbo",
        #I think this is the messages for the bot.
        messages = Query
    )

    #I dunno :). I think it's like the output or something.
    gpt_message = result["choices"][0]["message"]

    #Open MemoryFile for appending.
    with open(MemoryFile, "a") as fp:
        #M is the AI's response.
        M = {"role": gpt_message["role"], "content": gpt_message["content"]}

        #If the MemoryFile ain't blank then write ', ' yay. This is in order to prepare for the next appending I believe of like memory.
        if os.path.getsize(MemoryFile) != 0:
            fp.write(", ");
        #Write '[' because I believe that's how it's supposed to start the memory file.
        else:
            fp.write("[");

        #Write M to the file.
        json.dump(M, fp)
        #Write ']' to say that the file is over now file is over party trolled.
        fp.write("]");

    #Add the uh stuff to message_history like the Ai's response I think.
    message_history.append({"role": gpt_message["role"], "content": gpt_message["content"]})
    #Return what the Chatbot said and boom we're done with Talkers I think.
    return gpt_message["content"];


#The stuff that makes the bot work. It's a class and it uh uses the Client I think.
class MyClient(discord.Client):
    #When ready.
    async def on_ready(self):
        #Print this. Self is the bot.
        print("Logged on as", self.user)

    #When a message is received.
    async def on_message(self, message):

        #If it's a message from the bot itself.
        if message.author == self.user:
            #Ignore and end function.
            return

        #If the message is in the channel you want the bot to pay attention to. (If you want it to talk anywhere you can just remove this line then fix indents I think.).
        if message.channel.name == ChannelName:
            #If the message starts with the character to ignore.
            if message.content.startswith(IgnoreChar):
                #Ignore.
                pass
            #If it doesn't start with the character to ignore.
            else:
                #Output = Talkers yoooo.
                Output = Talkers(
                            #The Personality for Talkers is set to the Personality Variable that you hopefully set.
                            Personality = PersonalityVar,
                            #TellU or Tell User is set to print out whatever the bot uh does I think.
                            TellU = print,
                            #This is the formatting for the messages that the bot receives.
                            AskU = "Username : " + message.author.name + " ::: Message : " + message.content
                )

                #Send output to channel.
                await message.channel.send(Output)

#I don't know what this stuff does I think but it's fine I'll just assume?
#I think this sets a variable to be the Discord default Intents.
intents = discord.Intents.default()
#This shows that you have a messages intent so like you intend to receive messages with the bot.
intents.messages = True
#Client is equal to the thing we set up and the intents of the client involve the messages intent we just set up.
client = MyClient(intents=intents)
#Bada bing bada boom run that silly Bot with the key you hopefully set earlier.
client.run(BotKey);

#And bang there's the bot hopefully you enjoyed reading my comments if you read through them all. Uh. Yeah. Okay Cyvr out I suppose? Bye.