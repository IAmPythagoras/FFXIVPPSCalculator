#########################################
########## WHITEMAGE PLAYER #############
#########################################
from Jobs.Base_Spell import DOTSpell, empty, ManaRequirement
from Jobs.Healer.Healer_Spell import WhitemageSpell
import copy

#Requirement

def PresenceOfMindRequirement(Player, Spell):
    return Player.PresenceOfMindCD <= 0, Player.PresenceOfMindCD

def AssizeRequirement(Player, Spell):
    return Player.AssizeCD <= 0, Player.AssizeCD

def ThinAirRequirement(Player, Spell):
    return Player.ThinAirCD <= 0, Player.ThinAirCD

def BellRequirement(Player, Spell):
    return Player.BellCD <= 0, Player.BellCD

def AquaveilRequirement(Player, Spell):
    return Player.AquaveilCD <= 0, Player.AquaveilCD

def TemperanceRequirement(Player, Spell):
    return Player.TemperanceCD <= 0, Player.TemperanceCD

def PlaneryIndulgenceRequirement(Player, Spell):
    return Player.PlaneryIndulgenceCD <= 0, Player.PlaneryIndulgenceCD

def DivineBenisonRequirement(Player, Spell):
    return Player.DivineBenisonCD <= 0, Player.DivineBenisonCD

def TetragrammatonRequirement(Player, Spell):
    return Player.TetragrammatonCD <= 0, Player.TetragrammatonCD

def BenedictionRequirement(Player, Spell):
    return Player.BenedictionCD <= 0, Player.BenedictionCD

def AsylumRequirement(Player, Spell):
    return Player.AsylumCD <= 0, Player.AsylumCD

def BloodLilyRequirement(Player, Spell):
    return Player.LilyStack > 0, Player.LilyTimer

def BloomLilyRequirement(Player, Spell):
    return Player.BloomLily, -1



#Apply

def ApplyAfflatusMisery(Player, Enemy):
    Player.BloomLily = False
    Player.UsedLily = 0 #Reset counter

def ApplyLily(Player, Enemy):
    if not Player.BloomLily : Player.UsedLily = min(3, Player.UsedLily + 1)
    Player.LilyStack -= 1

    if Player.UsedLily == 3: Player.BloomLily = True

def Apply(Player, Enemy):
    Player.CD = 0

def ApplyBell(Player, Enemy):
    Player.BellCD = 180

def ApplyAquaveil(Player, Enemy):
    Player.AquaveilCD = 60

def ApplyTemperance(Player, Enemy):
    Player.TemperanceCD = 120

def ApplyPlaneryIndulgence(Player, Enemy):
    Player.PlaneryIndulgenceCD = 60

def ApplyDivineBenison(Player, Enemy):
    Player.DivineBenisonCD = 30

def ApplyTetragrammaton(Player, Enemy):
    Player.TetragrammatonCD = 60

def ApplyAsylum(Player, Enemy):
    Player.AsylumCD = 90

def ApplyBenediction(Player, Enemy):
    Player.BenedictionCD = 180

def ApplyDia(Player, Enemy):
    Player.DiaTimer = 30

    if (Player.Dia == None) : 
        Player.Dia = copy.deepcopy(DiaDOT)
        Player.EffectCDList.append(CheckDia)
        Player.DOTList.append(Player.Dia)

def ApplyAssize(Player, Enemy):
    Player.Mana = min(10000, Player.Mana + 500)
    Player.AssizeCD = 45

def ApplyThinAir(Player, Enemy):
    Player.ThinAirCD = 60
    Player.EffectList.append(ThinAirEffect)

def ApplyPresenceOfMind(Player, Enemy):
    Player.PresenceOfMindCD = 120
    Player.PresenceOfMindTimer = 15
    Player.EffectList.append(PresenceOfMindEffect)
    Player.EffectCDList.append(CheckPresenceOfMind)

#Effect

def ThinAirEffect(Player, Spell):
    Spell.ManaCost = 0
    Player.EffectList.remove(ThinAirEffect)

def PresenceOfMindEffect(Player, Spell):
    Spell.CastTime *= 0.8
    Spell.RecastTime *= 0.8

#Check

def CheckDia(Player, Enemy):
    if Player.DiaTimer <= 0:
        Player.DOTList.remove(Player.Dia)
        Player.Dia = None
        Player.EffectToRemove.append(CheckDia)

def CheckPresenceOfMind(Player, Enemy):
    if Player.PresenceOfMindTimer <= 0:
        Player.EffectList.remove(PresenceOfMindEffect)
        Player.EffectToRemove.append(CheckPresenceOfMind)



#Damage GCD
Glare = WhitemageSpell(1, True, 1.5, 2.5, 310, 400, empty, [ManaRequirement])
Dia = WhitemageSpell(2, True, 0, 2.5, 0, 400, ApplyDia, [ManaRequirement])
DiaDOT = DOTSpell(5, 60, False)
AfflatusMisery = WhitemageSpell(3, True, 0, 2.5, 1240, 0, ApplyAfflatusMisery, [BloomLilyRequirement])
Holy = WhitemageSpell(4, True, 2.5, 2.5, 150, 400, empty, [ManaRequirement])
#Healing GCD
AfflatusRapture = WhitemageSpell(5, True, 0, 2.5, 0, 0, ApplyLily, [BloodLilyRequirement])
AfflatusSolace = WhitemageSpell(6, False, 0, 0, 0, 0, ApplyLily, [BloodLilyRequirement])
Medica2 = WhitemageSpell(7, True, 2, 2.5, 0, 1000, empty, [ManaRequirement])
Regen = WhitemageSpell(8, True, 0, 2.5, 0, 400, empty, [ManaRequirement])
Cure = WhitemageSpell(9, True, 1.5, 2.5, 0, 400, empty, [ManaRequirement])
Cure2 = WhitemageSpell(10, True, 2, 2.5, 0, 1000, empty, [ManaRequirement])
Cure3 = WhitemageSpell(11, True, 2, 2.5, 0, 1500, empty, [ManaRequirement])
Medica = WhitemageSpell(12, True, 2, 2.5, 0, 900, empty, [ManaRequirement])
#Damage oGCD
Assize = WhitemageSpell(13, False, 0, 0, 400, 0, ApplyAssize, [AssizeRequirement])
ThinAir = WhitemageSpell(14, False, 0, 0, 0, 0, ApplyThinAir, [ThinAirRequirement])
PresenceOfMind = WhitemageSpell(15, False, 0, 0, 0, 0, ApplyPresenceOfMind, [PresenceOfMindRequirement])

#Healing oGCD
Bell = WhitemageSpell(16, False, 0, 0, 0, 0, ApplyBell, [BellRequirement]) #Litturgy of the bell
Aquaveil = WhitemageSpell(17, False, 0, 0, 0, 0, ApplyAquaveil, [AquaveilRequirement])
Temperance = WhitemageSpell(18, False, 0, 0, 0, 0, ApplyTemperance, [TemperanceRequirement])
PlaneryIndulgence = WhitemageSpell(19, False, 0, 0, 0, 0, ApplyPlaneryIndulgence, [PlaneryIndulgenceRequirement])
DivineBenison =WhitemageSpell(20, False, 0, 0, 0, 0, ApplyDivineBenison, [DivineBenisonRequirement])
Tetragrammaton = WhitemageSpell(21, False, 0, 0, 0, 0, ApplyTetragrammaton, [TetragrammatonRequirement])
Asylum = WhitemageSpell(22, False, 0, 0, 0, 0, ApplyAsylum, [AsylumRequirement])
Benediction = WhitemageSpell(23, False, 0, 0, 0, 0, ApplyBenediction, [BenedictionRequirement])

WhiteMageAbility = {}