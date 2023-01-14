import time
import serial
import adafruit_fingerprint
import cx_Oracle as cx
from datetime import datetime
#import datetime
from pprint import pprint 
import pandas as pd
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
def get_fingerprint():
    """Preuzimanje otiska,templetiranje,usporedba"""
    print("Prislonite prst ...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Skeniram...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Tražim...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Preuzimanje otiska,templetiranje,usporedba sa detaljima"""
    print("Skeniram", end="", flush=True)
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Skenirano")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("Nema prepoznatog prsta")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imagefail error")
        else:
            print("Drugi error")
        return False

    print("Skeniram...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Skenirano")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Slika je mutna")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Ne mogu prepoznati detalje")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Pogreška")
        else:
            print("Drugi error")
        return False

    print("Tražim...", end="", flush=True)
    i = finger.finger_fast_search()
    if i == adafruit_fingerprint.OK:

        print("Otisak nađen!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("Otisak se ne podudara")
        else:
            print("Drugi error")
        return False

# pylint: disable=too-many-statements
def enroll_finger(location):
    """uzmi dvje slike napravi template i spremi u location"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Stavi prst na senzor...", end="", flush=True)
        else:
            print("Stavi isti prst opet...", end="", flush=True)
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Slika spremljena")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Greška u slici")
                return False
            else:
                print("Drugi error")
                return False

        print("Molimo pričekajte...", end="", flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Spremljeno")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Slika je mutna")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Ne mogu prepoznati detalje")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Pogreška u slici")
            else:
                print("Drugi error")
            return False
        if fingerimg == 1:
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Kreiram model...", end="", flush=True)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Kreiran")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Otisci se ne podudaraju")
        else:
            print("Drugi error")
        return False

    print("Spremam model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Spremljen")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Pogrešna lokacija")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Error na kartici")
        else:
            print("Drugi error")
        return False
    get_fingerprint()
    return True


def save_fingerprint_image(filename):
    """Skeniraj prst i spremi sliku kao file."""
    while finger.get_image():
        pass
    from PIL import Image  # pylint: disable=import-outside-toplevel

    img = Image.new("L", (256, 288), "white")
    pixeldata = img.load()
    mask = 0b00001111
    result = finger.get_fpdata(sensorbuffer="image")

    x = 0
    y = 0
    for i in range(len(result)):
        pixeldata[x, y] = (int(result[i]) >> 4) * 17
        x += 1
        pixeldata[x, y] = (int(result[i]) & mask) * 17
        if x == 255:
            x = 0
            y += 1
        else:
            x += 1

    if not img.save(filename):
        return True
    return False
##################################################
def get_num(max_number):
    """Main!"""
    i = 1
    return i


myGlobal = 0

def isOpen():
    try:
        global myGlobal
        myGlobal = 1
        #return db.ping() is None
        return 1
    except:
        myGlobal = 0
        print('nista')
        #exc(finger.finger_id)
        return 0


def upis(positionNumber):
    global db
    print('nista1')
    try:
    """
        need to add this lines as connection string
        db = cx.connect('DATABASE USERNAME', 'DATABASE PASSWORD', 'DATABASE IP:UDATABASE PORT/DATABASE NAME')
        dsn_tns = cx.makedsn('DATABASE IP', UDATABASE PORT, 'DATABASE NAME')
    """
        cur = db.cursor()
        print(cur)
    except (cx.DatabaseError):
        print('nista2')
        #excell
    isOpen()
    print(myGlobal)
    if myGlobal==1:
        dtime=datetime.now()
        d=positionNumber
        print(cur)
        vr='RR'
        appm='ČITAČ broj:1'
        cur.prepare( "INSERT INTO tev_evid(r_id,r_id_edit,ulaz,vrsta_r,app_msg) values (:t,:ed,:ts,:vr,:app)" )
        cur.setinputsizes(ts=cx.TIMESTAMP)
        cur.execute(None, {'t':d,'ed':d,'ts':dtime,'vr':vr,'app':appm})
        print(db.ping())
        db.commit()
        db.close()
    elif myGlobal==0:
        print('ne valja')
        excell(positionNumber)


def excell():
    data = finger.finger_id
    print(dt_string)
    with pd.ExcelWriter('my_oracle_table.xlsx') as writer:
        data.to_excel(writer)
        time.sleep(60.4)

    with pd.ExcelWriter('my_oracle_table.xlsx') as writer:
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string)
        data.to_excel(writer)        
    return True
    
"""
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(22,GPIO.RISING,callback=enroll_finger) # Setup eve
"""
while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Greška učitavanju predloška")
    print("Iskorištene pozicije: ", finger.templates)
    if finger.count_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Greška učitavanju predloška")
    print("Broj spremljenih prstiju: ", finger.template_count)
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        raise RuntimeError("Greška u sistemskim parametrima")
    print("e) Dodavanje")
    print("f) Traženje")
    print("d) Brisanje")
    print("s) Spremanje slike")
    print("r) reset ")
    print("q) izlaz")
    print("----------------")
    c = input("> ")

    if c == "e":
        enroll_finger(get_num(finger.library_size))
    if c == "f":
        if get_fingerprint():
            print("Nađen #", finger.finger_id, "sa pouzdanoscu", finger.confidence)
            upis(finger.finger_id)
        else:
            print("Prst nije nađen")
    if c == "d":
        if finger.delete_model(get_num(finger.library_size)) == adafruit_fingerprint.OK:
            print("Izbrisan!")
        else:
            print("Greška u brisanju")
    if c == "s":
        if save_fingerprint_image("fingerprint.png"):
            print("Slika spremljena")
        else:
            print("Greška u spremanju slike")
    if c == "r":
        if finger.empty_library() == adafruit_fingerprint.OK:
            print("Biblioteka prazna!")
        else:
            print("Greška u brisanju")
    if c == "q":
        print("Izlazim :(")
        raise SystemExit
