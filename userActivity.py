import time
jsm = __import__("jsonmanager")


class UserActivityClass:
    def __init__(self, jsonFile, role, bot):
        self.jsonFile = jsonFile
        self.jsonManager = jsm.JsonManager(self.jsonFile)
        self.ExpireTime = self.jsonManager.load()["ActiveRoleExpireTime"]
        self.role = role
        self.bot = bot
        self.version = 2.0

    def newUser(self, id, name):
        self.file = self.jsonManager.load()
        self.file["users"][id] = {"name":name, "points":0, "lastMessageTimestamp":time.time()} 
        self.jsonManager.save(self.file)

    def removeUser(self, id):
        pass

    def updateFileFormat(self):
        self.file = self.jsonManager.load()
        print("reading version")
        if(self.file["version"] != self.version):
            print("needs version update")
            for i in self.file["users"]:
                self.file["users"][i]["points"] = 7.5 if (self.file["users"][i]["lastMessageTimestamp"] > time.time() - self.ExpireTime) else 0
        else:
            print("file doesnt need updating")
        self.file["version"] = self.version
        self.jsonManager.save(self.file)
        

    def addScore(self, score): # removes 1 point from everyone.
        self.file = self.jsonManager.load()
        
        for i in self.file["users"]:
            self.file["users"][i]["points"] += score
            self.file["users"][i]["points"] = max(self.file["users"][i]["points"], 0)
            self.file["users"][i]["points"] = min(self.file["users"][i]["points"], 10)

        
        self.jsonManager.save(self.file)

    
        


    def updateActivity(self, id, name):
        self.file = self.jsonManager.load()
        id = str(id)
        messageSpamTimeout = 30 #in seconds, used to not add points while a user is spamming
        try:
            self.file["users"][id]["name"] = name

            if(self.file["users"][id]["lastMessageTimestamp"] < time.time() - messageSpamTimeout): #prevent message spam to add up points too quickly
                self.file["users"][id]["points"] += 1
                self.file["users"][id]["lastMessageTimestamp"] = time.time()

            self.file["users"][id]["points"] = min(self.file["users"][id]["points"], 10) #max a users points at 10
        except:
            self.newUser(id, name)
        self.jsonManager.save(self.file)

        return self.file["users"][id]["points"] >= 5

        



    