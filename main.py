from slowprint import slowprint
import apiConnect
import keyboard
import os

BANNER = '''
       /\              
      /##\ 
     /####\         $$\   $$\  $$$$$$\  $$\    $$\  $$$$$$\        $$$$$$$\  $$\   $$\ $$$$$$$\  $$\   $$\ $$\      $$\ $$\   $$\ 
    /######\        $$ |  $$ |$$  __$$\ $$ |   $$ |$$  __$$\       $$  __$$\ $$ |  $$ |$$  __$$\ $$ |  $$ |$$$\    $$$ |$$ |  $$ |
   /########\       $$ |  $$ |$$ /  $$ |$$ |   $$ |$$ /  $$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$$$\  $$$$ |$$ |  $$ |
  /##########\      $$$$$$$$ |$$$$$$$$ |\$$\  $$  |$$$$$$$$ |      $$ |  $$ |$$ |  $$ |$$$$$$$  |$$ |  $$ |$$\$$\$$ $$ |$$ |  $$ |
 /############\     $$  __$$ |$$  __$$ | \$$\$$  / $$  __$$ |      $$ |  $$ |$$ |  $$ |$$  __$$< $$ |  $$ |$$ \$$$  $$ |$$ |  $$ |
/##############\    $$ |  $$ |$$ |  $$ |  \$$$  /  $$ |  $$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$  /$$ |$$ |  $$ |
\##############/    $$ |  $$ |$$ |  $$ |   \$  /   $$ |  $$ |      $$$$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$  |$$ | \_/ $$ |\$$$$$$  |
 \############/     \__|  \__|\__|  \__|    \_/    \__|  \__|      \_______/  \______/ \__|  \__| \______/ \__|     \__| \______/ 
  \##########/
   \########/
    \######/
     \####/
      \##/
       \/


'''
is_hotkey_sent=False
is_current=False
is_forecast=False
is_suggester=False
is_exit=False
query=""

def on_current():
        global is_hotkey_sent
        global is_current
        is_hotkey_sent = True
        is_current = True
        
        
def on_forecast():
        global is_hotkey_sent
        global is_forecast
        is_hotkey_sent = True
        is_forecast=True
        
def on_suggest():
        global is_hotkey_sent
        global is_suggester
        is_hotkey_sent = True
        is_suggester=True
        
def on_exit():
        global is_hotkey_sent
        global is_exit
        is_hotkey_sent = True
        is_exit=True
        
keyboard.register_hotkey('alt+c', on_current)
keyboard.register_hotkey('alt+f', on_forecast)
keyboard.register_hotkey('alt+q', on_exit)

def showCurrent():
    global query
    query = getInput()
    currentData = apiConnect.pullCurrent(query)
    if(currentData['status']==0):
        forecastBanner = f'''
{currentData['location']['country']}, {currentData['location']['region']}, {currentData['location']['name']} Hava Durumu:
{currentData['weather']['condition']}
Sıcaklık: {currentData['weather']['temp']}°C
Nem: %{currentData['weather']['humidity']}
Bulutluluk: %{currentData['weather']['cloud']}
        '''
        print(forecastBanner)
    else:
        print('Hatalı Şehir Adı Girdiniz!')
        showCurrent()
        
def showForecast():
    global query
    query = getInput()
    forecastData = apiConnect.pullForecast(query)
    forecastList =[]
    forecastAlign =[]
    forecastRow = []
    if(forecastData['status']==0):
        for cast in forecastData['forecast']:
            forecastRow = [cast['time'][11:],cast['condition'],str(cast['temp'])+"°C",'%'+str(cast['humidity'])]
            forecastList.append(forecastRow)
        
        forecastList.insert(0,["Saat","Hava Durumu","Sıcaklık","Nem"])
        
            
        max_width = max([len(str(tableCell)) for row in forecastList for tableCell in row])
        print(f"{forecastData['location']['country']}, {forecastData['location']['region']}, {forecastData['location']['name']} Hava Durumu:")
        for row in forecastList:
            print("     ".join([str(tableCell).ljust(max_width) for tableCell in row]))
            
    else:
        print('Hatalı Şehir Adı Girdiniz!')
        showForecast()
    

def suggest():
    global query
    data = apiConnect.pullSuggestEssentials(query)
    if(data['status']==0):
        hardcorewear=False
        hardwear=False
        midwear=False
        easywear=False
        lightwear=False
        overUV=False
        overheat=False
        rain=False
        snow=False
        
        
        if(5>=data['avgtemp']):
            hardcorewear = True
        elif(15>=data['avgtemp']>5):
            hardwear = True
        elif(25>=data['avgtemp']>15):
            midwear = True
        elif(30>=data['avgtemp']>25):
            easywear = True
        elif(35>=data['avgtemp']>30):
            lightwear = True
        else:
            overheat = True
            
        if(data['willRain']==1):
            rain = True
        if(data['willSnow']==1):
            snow = True
        if(data['uv']>6.5):
            overUV = True
            
        if(overheat == True):
            print('Çok sıcak dışarı çıkmanız tavsiye edilmez, bol su için.')
    
        if(overUV == True):
            print("UV değerleri çok yüksek dışarı çıkmanız tavsiye edilmez.")
            
        if(hardcorewear==True and snow==True):
            print("Kaydırmaz bot ve kar kabanı giyiniz.")
        elif(hardcorewear==True and rain == True):
            print("Çok kalın ve su geçirmez şeyler giyiniz.")
        elif(hardcorewear==True):
            print("Çok kalın şeyler giyiniz.")
        elif(hardwear == True and snow==True ):
            print("Kaydırmaz bot ve kar kabanı giyiniz.")
        elif(hardwear == True and rain==True ):
            print("Su geçirmez kalın şeyler giyiniz.")
        elif(hardwear == True):
            print("Kalın şeyler giyiniz.")
        elif(midwear == True and rain==True ):
            print("Orta-kalın yağmurluk giyiniz.")
        elif(midwear == True):
            print("Orta-kalın şeyler giyiniz.")
        elif(easywear == True and rain==True ):
            print("Orta-ince yağmurluk giyiniz.")
        elif(easywear == True):
            print("Orta-ince şeyler giyiniz.")
        elif(lightwear == True and rain==True ):
            print("İnce yağmurluk giyiniz.")
        elif(lightwear == True):
            print("İnce şeyler giyiniz.")
        
    else:
        print('API hatası')
    

def getCommand():
   
    global is_hotkey_sent
    global is_forecast
    global is_current
    global is_exit
    global is_suggester
    
    commandList ='''Mevcut hava durumu ALT-C            Günlük hava dumunu ALT-F              Kıyafet önerisi ALT-S             Çıkış ALT-Q'''
    print(commandList)
    while True:
        if(is_hotkey_sent==True):
            os.system('cls')
            is_hotkey_sent=False
            break
    if(is_current==True):
        is_current=False
        showCurrent()
    if(is_forecast==True):
        is_forecast=False
        showForecast()
    if(is_suggester==True):
        is_suggester=False
        suggest()
    if(is_exit==True):
        exit(0)
        


def getInput():
    keyboard.remove_all_hotkeys()
    user =  input("Hava durumunu istediğiniz bölgeyi giriniz: ")
    keyboard.register_hotkey('alt+c', on_current)
    keyboard.register_hotkey('alt+f', on_forecast)
    keyboard.register_hotkey('alt+s', on_suggest)
    keyboard.register_hotkey('alt+q', on_exit)
    return user

def main():
    showBanner()
    showCurrent()
    while True:
        
        getCommand()

def showBanner():
    slowprint.slowprint(BANNER,.025)
    
main()