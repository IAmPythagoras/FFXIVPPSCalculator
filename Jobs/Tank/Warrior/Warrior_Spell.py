#########################################
########## WARRIOR Spell  ###############
#########################################

from Jobs.Base_Spell import buff, empty
from Jobs.Tank.Tank_Spell import WarriorSpell
Lock = 0.75

def BeastGaugeRequirement(Player, Spell):
    RemoveBeast(Player, Spell.Cost)
    return Player.BeastGauge >= 0, -1

#Special

def AddBeast(Player, Gauge):
    Player.BeastGauge = min(100, Player.BeastGauge + Gauge)

def RemoveBeast(Player, Gauge):
    Player.BeastGauge -= Gauge #Caanot go under 0 cuz verify if enough gauge

#Requirement

def UpheavalRequirement(Player, Spell):
    return Player.UpheavalCD <= 0, Player.UpheavalCD

def OnslaughtRequirement(Player, Spell):
    return Player.OnslaughtStack >= 1, Player.OnslaughtCD

def InfuriateRequirement(Player, Spell):
    return Player.InfuriateStack >= 1, Player.InfuriateCD

def InnerReleaseRequirement(Player, Spell):
    return Player.InnerReleaseCD <= 0, Player.InnerReleaseCD

def PrimalRendRequirement(Player, Spell):
    return Player.PrimalRendTimer > 0, -1

def FellCleaveRequirement(Player, Spell):
    return Player.BeastGauge >= 50, -1

def InnerChaosRequirement(Player, Spell):
    return Player.NascentChaosTimer > 0, -1

def ThrillOfBattleRequirement(Player, Spell):
    return Player.ThrillOfBattleCD <= 0, Player.ThrillOfBattleCD

def HolmgangRequirement(Player, Spell):
    return Player.HolmgangCD <= 0, Player.HolmgangCD

def ShakeItOffRequirement(Player, Spell):
    return Player.ShakeItOffCD <= 0, Player.ShakeItOffCD

def NascentFlashRequirement(Player, Spell):
    return Player.NascentFlashCD <= 0, Player.NascentFlashCD

def BloodwhettingRequirement(Player, Spell):
    return Player.BloodwhettingCD <= 0, Player.BloodwhettingCD

def EquilibriumRequirement(Player, Spell):
    return Player.EquilibriumCD <= 0, Player.EquilibriumCD

#Apply

def ApplyEquilibrium(Player, Enemy):
    Player.EquilibriumCD = 60

def ApplyBloodwhetting(Player, Enemy):
    Player.BloodwhettingCD = 25

def ApplyNascentFlash(Player, Enemy):
    Player.NascentFlashCD = 25

def ApplyShakeItOff(Player, Enemy):
    Player.ShakeItOffCD = 90

def ApplyHolmgang(Player, Enemy):
    PlayerHolmgangCD = 240

def ApplyThrillOfBattle(Player, Enemy):
    Player.ThrillOfBattleCD = 90

def ApplyOverpower(Player, Enemy):
    if not (OverpowerCombo in Player.EffectList) : Player.EffectList.append(OverpowerCombo)

def ApplyHeavySwing(Player, Enemy):
    if not (HeavySwingEffect in Player.EffectList) : Player.EffectList.append(HeavySwingEffect)

def ApplyMaim(Player, Enemy):
    if not (MaimEffect in Player.EffectList) : Player.EffectList.append(MaimEffect)
    AddBeast(Player, 10)

def ApplyStormEye(Player, Enemy):
    Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 30)
    AddBeast(Player, 10)

def ApplyStormPath(Player, Enemy):
    AddBeast(Player, 20)

def ApplyUpheaval(Player, Enemy):
    Player.UpheavalCD = 30

def ApplyOnslaught(Player, Enemy):
    if Player.OnslaughtStack == 3:
        #Then we have to add check
        Player.EffectCDList.append(OnslaughtStackCheck)
        Player.OnslaughtCD = 30
    Player.OnslaughtStack -= 1

def ApplyInfuriate(Player, Enemy):
    AddBeast(Player, 50)
    if Player.InfuriateStack == 2:
        Player.EffectCDList.append(InfuriateStackCheck)

    Player.InfuriateStack -= 1
    Player.NascentChaosTimer = 30

def ApplyInnerRelease(Player, Enemy):
    Player.EffectList.append(InnerReleaseEffect)
    Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 10)
    Player.PrimalRendTimer = 30 #Primal rend ready
    Player.InnerReleaseStack = 3
    Player.NoBeastCostStack = 3
    Player.InnerReleaseCD = 60

def ApplyPrimalRend(Player, Enemy):
    Player.InnerReleaseStack += 1 #To allow for Direct Crit
    Player.PrimalRendTimer = 0

def ApplyInnerChaos(Player, Enemy):
    Player.InnerReleaseStack += 1
    Player.InfuriateCD = max(0, Player.InfuriateCD - 5)
    Player.NascentChaosTimer = 0

#Effect

def InnerReleaseEffect(Player, Spell):
    if isinstance(Spell, WarriorSpell) and Spell.Cost != 0:
        Player.NoBeastCostStack -= 1
        Spell.Cost = 0
        if Player.NoBeastCostStack == 0: 
            Player.EffectToRemove.append(InnerReleaseEffect)

def SurgingTempestEffect(Player, Spell):
    if Player.SurgingTempestTimer > 0 : 
        Player.buffList.append(SurgingTempestBuff)
        Player.EffectCDList.append(SurgingTempestCheck)
        Player.EffectToRemove.append(SurgingTempestEffect)

#Combo Action

def OverpowerCombo(Player, Spell):
    if Spell.id == MythrilTempest.id:
        Spell.Potency += 50
        Player.SurgingTempestTimer = min(60, Player.SurgingTempestTimer + 30)
        Player.EffectToRemove.append(OverpowerCombo)

def HeavySwingEffect(Player, Spell):
    if Spell.id == 2:
        Spell.Potency += 150
        Player.EffectToRemove.append(HeavySwingEffect)

def MaimEffect(Player, Spell):
    if Spell.id == 3 or Spell.id == 11:
        Spell.Potency += 280
        Player.EffectToRemove.append(MaimEffect)


#Check

def SurgingTempestCheck(Player, Enemy):
    if Player.SurgingTempestTimer <= 0: 
        Player.buffList.remove(SurgingTempestBuff)
        Player.EffectList.append(SurgingTempestEffect)
        Player.EffectToRemove.append(SurgingTempestCheck)

def OnslaughtStackCheck(Player, Enemy):
    if Player.OnslaughtCD <= 0:
        if Player.OnslaughtStack == 2:
            Player.EffectToRemove.append(OnslaughtStackCheck)
        else:
            Player.OnslaughtCD = 30
        Player.OnslaughtStack += 1

def InfuriateStackCheck(Player, Enemy):
    if Player.InfuriateCD <= 0:
        if Player.InfuriateStack == 1:
            Player.EffectToRemove.append(InfuriateStackCheck)
        else:
            Player.InfuriateCD = 30
        Player.InfuriateStack += 1
    

#Combo Action
HeavySwing = WarriorSpell(1, True, Lock, 2.5, 200, 0, ApplyHeavySwing, [],0)
Maim = WarriorSpell(2, True, Lock, 2.5, 130, 0, ApplyMaim, [],0)
StormEye = WarriorSpell(3, True, Lock, 2.5, 120, 0, ApplyStormEye, [],0)
StormPath = WarriorSpell(4, True, Lock, 2.5, 120, 0, ApplyStormPath, [], 0)
#Missing Storm's path

#oGCD
Upheaval = WarriorSpell(5, False, Lock, 0, 350, 0, ApplyUpheaval, [UpheavalRequirement],0)
Onslaught = WarriorSpell(6, False, Lock, 0, 150, 0, ApplyOnslaught, [OnslaughtRequirement],0)
Infuriate = WarriorSpell(7, False, Lock, 0, 0, 0, ApplyInfuriate, [InfuriateRequirement],0)
InnerRelease = WarriorSpell(8, False, Lock, 0, 0, 0, ApplyInnerRelease, [InnerReleaseRequirement],0)


#GCD
PrimalRend = WarriorSpell(9, True, Lock, 2.5, 700, 0, ApplyPrimalRend, [PrimalRendRequirement],0)
FellCleave = WarriorSpell(10, True, Lock, 2.5, 460, 0, empty, [],50)
InnerChaos = WarriorSpell(11, True, Lock, 2.5, 650,0, ApplyInnerChaos, [InnerChaosRequirement], 50)
Tomahawk = WarriorSpell(12, True, Lock, 2.5, 150, 0, empty, [], 0)

#AOE GCD
Overpower = WarriorSpell(13,True, 0, 2.5, 110, 0 , ApplyOverpower, [], 0 )
MythrilTempest = WarriorSpell(14, True, 0, 2.5, 100, 0, empty, [], 0)
Decimate = WarriorSpell(15, True, 0, 2.5, 200, 0, empty, [], 50)
ChaoticCyclone = WarriorSpell(16, True, Lock, 2.5, 320,0, ApplyInnerChaos, [InnerChaosRequirement], 50) #AOE Version of Inner chaos
#AOE oGCD
Orogeny = WarriorSpell(17, False, Lock, 0, 150, 0, ApplyUpheaval, [UpheavalRequirement],0) #AOE Version of Upheaval
#Mit
ThrillOfBattle = WarriorSpell(18, False, 0, 0, 0, 0, ApplyThrillOfBattle, [ThrillOfBattleRequirement], 0)
Holmgang = WarriorSpell(19, False, 0, 0, 0, 0, ApplyHolmgang, [HolmgangRequirement], 0)
ShakeItOff = WarriorSpell(20, False, 0, 0, 0, 0, ApplyShakeItOff, [ShakeItOffRequirement], 0)
NascentFlash = WarriorSpell(21, False, 0, 0, 0, 0, ApplyNascentFlash, [NascentFlashRequirement], 0)
Bloodwhetting = WarriorSpell(22, False, 0, 0, 0, 0, ApplyBloodwhetting, [BloodwhettingRequirement], 0)
Equilibrium = WarriorSpell(23, False, 0, 0, 0, 0, ApplyEquilibrium, [EquilibriumRequirement], 0)
#buff
SurgingTempestBuff = buff(1.1)

WarriorAbility = {}