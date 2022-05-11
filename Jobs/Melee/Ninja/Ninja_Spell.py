from tkinter.tix import Tree
from Jobs.Base_Spell import buff, empty
from Jobs.Melee.Melee_Spell import NinjaSpell
from Jobs.Melee.Ninja.Ninja_Spell import ArmorCrush
Lock = 0.75


#Requirement

def TenChiJinRequirement(Player, Spell):
    return Player.TenChiJinCD <= 0

def HyoshoRanryuRequirement(Player, Spell):
    return Player.Kassatsu

def KassatsuRequirement(Player, Spell):
    return Player.KassatsuCD <= 0

def NinjutsuRequirement(Player, Spell):
    return Player.NinjutsuStack > 0 or Player.Kassatsu

def FleetingRaijuRequirement(Player, Spell):
    return Player.RaijuStack > 0

def MeisuiRequirement(Player, Spell):
    return Player.Suiton and Player.MeisuiCD <= 0

def BhavacakraRequirement(Player, Spell):
    return Player.NinkiGauge >= 50

def TrickAttackRequirement(Player, Spell):
    return Player.Suiton and Player.TrickAttackCD <= 0

def MugRequirement(Player, Spell):
    return Player.MugCD <= 0

def DreamWithinADreamRequirement(Player, Spell):
    return Player.DreamWithinADreamCD <= 0

#Apply

def ApplyKassatsu(Player, Enemy):
    Player.KassatsuTimer = 15
    Player.KassatsuCD = 60
    Player.EffectList.append(KassatsuEffect)
    Player.EffectCDList.append(KassatsuCheck)

def ApplyHyoshoRanryu(Player, Enemy):
    if not Player.Kassatsu: ApplyNinjutsu(Player, Enemy)
    else: Player.Kassatsu = False

def ApplySuiton(Player, Enemy):
    if not Player.Kassatsu: ApplyNinjutsu(Player, Enemy)
    else: Player.Kassatsu = False
    Player.Suiton = True
    if not SuitonCheck in Player.EffectCDList : Player.EffectCDList.append(SuitonCheck)
    Player.SuitonTimer = 20

def ApplyHuton(Player, Enemy):
    if not Player.Kassatsu: ApplyNinjutsu(Player, Enemy)
    else: Player.Kassatsu = False
    Player.HutonTimer = 60

def ApplyRaiton(Player, Enemy):
    if not Player.Kassatsu: ApplyNinjutsu(Player, Enemy)
    else: Player.Kassatsu = False

    if Player.RaijuStack == 0: Player.EffectList.append(RaitonEffect) #will loose all if weaponskill is done
    Player.RaijuStack = min(3, Player.RaijuStack + 1)

def ApplyNinjutsu(Player, Enemy):
    if Player.NinjutsuStack == 2:
        Player.EffectCDList.append(NinjutsuStackCheck)
        Player.NinjutsuCD = 20
    Player.NinjutsuStack -= 1

def ApplyThrowingDagger(Player, Enemy):
    Player.AddNinki(5)

def ApplyFleetingRaiju(Player, Enemy):
    Player.RaijuReady = False

def ApplyMeisui(Player, Enemy):
    Player.Suiton = False
    Player.AddNinki(50)
    Player.MeisuiCD = 120
    Player.MeisuiTimer = 30
    Player.EffectList.append(MeisuiEffect)
    Player.EffectCDList.append(MeisuiCheck)

def ApplyBhavacakra(Player, Enemy):
    Player.AddNinki(-50)

def ApplyTrickAttack(Player, Enemy):
    Player.buffList.append(TrickAttackBuff)
    Player.TrickAttackCD = 60
    Player.TrickAttackTimer = 15
    Player.EffectCDList.append(TrickAttackCheck)

def ApplyMug(Player, Enemy):
    Enemy.buffList.append(MugBuff)
    Player.MugCD = 120
    Player.MugTimer = 20
    Player.AddNinki(40)
    Player.EffectCDList.append(MugCheck)

def ApplyHuraijin(Player, Enemy):
    Player.HutonTimer = 60

def ApplyDreamWithinADream(Player, Enemy):
    Player.DreamWithinADreamCD = 60

def ApplySpinningEdge(Player, Enemy):
    Player.AddNinki(5)
    
    if not (SpinningEdgeCombo in Player.EffectList): Player.EffectList.append(SpinningEdgeCombo)


#Effect

def KassatsuEffect(Player, Spell):
    if Spell.Ninjutsu:
        Spell.DPSBonus = 1.3
        Player.EffectCDList.remove(KassatsuCheck)
        Player.EffectToRemove.append(KassatsuEffect)
        Player.Kassatsu = False

def RaitonEffect(Player, Spell):
    if Spell.Weaponskill or Player.RaijuStack == 0:
        Player.RaijuStack = 0
        Player.EffectToRemove.append(RaitonEffect)

def MeisuiEffect(Player, Spell):
    if Spell.id == Bhavacakra.id:
        Spell.Potency += 150

def SpinningEdgeCombo(Player, Spell):
    if Spell.id == GustSlash.id:
        Spell.Potency += 160
        Player.AddNinki(5)
        Player.EffectToRemove.append(SpinningEdgeCombo)
        if not (GustSlashCombo in Player.EffectList) : Player.EffectList.append(GustSlashCombo)

def GustSlashCombo(Player, Spell):
    if Spell.id == AeolianEdge.id:
        Spell.Potency += 240
        Player.AddNinki(15)
        Player.EffectToRemove.append(GustSlashCombo)
    elif Spell.id == ArmorCrush.id:
        Spell.Potency += 220
        Player.AddNinki(15)
        Player.AddHuton(30)
        Player.EffectToRemove.append(GustSlashCombo)


#Check

def SuitonCheck(Player, Enemy):
    if not Player.Suiton or Player.SuitonTimer <= 0:
        Player.EffectToRemove.append(SuitonCheck)
        Player.SuitonTimer = 0
        Player.Suiton = False

def KassatsuCheck(Player, Enemy):
    if Player.KassatsuTimer <= 0:
        Player.EffectList.remove(KassatsuEffect)
        Player.EffectToRemove.append(KassatsuCheck)
        Player.Kassatsu = False

def NinjutsuStackCheck(Player, Enemy):
    if Player.NinjutsuCD <= 0:
        if Player.NinjutsuStack == 1:
            Player.EffectToRemove.append(NinjutsuStackCheck)
        else:
            Player.NinjutsuCD = 20
        Player.NinjutsuStack +=1

def MeisuiCheck(Player, Enemy):
    if Player.MeisuiTimer <= 0:
        Player.EffectList.remove(MeisuiEffect)
        Player.EffectToRemove.append(MeisuiCheck)

def TrickAttackCheck(Player, Enemy):
    if Player.TrickAttackTimer <= 0:
        Player.buffList.remove(TrickAttackBuff)
        Player.EffectToRemove.append(TrickAttackCheck)

def MugCheck(Player, Enemy):
    if Player.MugTimer <= 0:
        Enemy.buffList.remove(MugBuff)
        Player.EffectToRemove.append(MugCheck)



#GCD
SpinningEdge = NinjaSpell(1, True, Lock, 2.5, 220, ApplySpinningEdge, [], True, False)
GustSlash = NinjaSpell(2, True, Lock, 2.5, 160, empty, [], True, False)
AeolianEdge = NinjaSpell(3, True, Lock, 2.5, 200, empty, [], True, False)
ArmorCrush = NinjaSpell(4, True, Lock, 2.5, 200, empty, [], True, False)
Huraijin = NinjaSpell(6, True, Lock, 2.5, 200, ApplyHuraijin, [], True, False)
FleetingRaiju = NinjaSpell(11, True, Lock, 2.5, 560, ApplyFleetingRaiju, [FleetingRaijuRequirement], True, False)
ThrowingDagger = NinjaSpell(12, True, Lock, 2.5, 120, ApplyThrowingDagger, [], True, False)

#Ninjutsu
FumaShuriken = NinjaSpell(13, True, 1 + Lock, 1 + 1.5, 450, ApplyNinjutsu, [NinjutsuRequirement], False, True) 
Raiton = NinjaSpell(14, True, 2 + Lock, 1 + 1 + 1.5, 650, ApplyRaiton, [NinjutsuRequirement], False, True )
Huton = NinjaSpell(15, True, 3 + Lock, 3 + 1.5, 0, ApplyHuton, [NinjutsuRequirement], False, True)
Suiton = NinjaSpell(16, True, 3 + Lock, 3 + 1.5, 500, ApplySuiton, [NinjutsuRequirement], False, True)
HyoshoRanryu = NinjaSpell(17, True, 3 + Lock, 3 + 1.5, 1300, ApplyHyoshoRanryu, [HyoshoRanryuRequirement], False, True)

TenChiJin = NinjaSpell(18, False, Lock, 0, 0, ApplyTenChiJin, [TenChiJinRequirement], False, False)

#oGCD
DreamWithinADream = NinjaSpell(5, False, Lock, 0, 3*150, ApplyDreamWithinADream, [DreamWithinADreamRequirement], False, False)
Mug = NinjaSpell(7, False, Lock, 0, 150, ApplyMug, [MugRequirement], False, False)
TrickAttack = NinjaSpell(8, False, Lock, 0, 400, ApplyTrickAttack, [TrickAttackRequirement], False, False)
Bhavacakra = NinjaSpell(9, False, Lock, 0, 350, ApplyBhavacakra, [BhavacakraRequirement], False, False)
Meisui = NinjaSpell(10, False, Lock, 0, 0, ApplyMeisui, [MeisuiRequirement], False, False)


#buff
MugBuff = buff(1.05)
TrickAttackBuff = buff(1.1)