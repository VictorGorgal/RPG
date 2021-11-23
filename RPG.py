import random
from os import system
from time import sleep


class mage:
    def __init__(self):
        self.lifebase = 20
        self.level = 1
        self.armorbase = 5
        self.armor = 5
        self.damagebase = 10
        self.damage = 10
        self.XP = 0
        self.XPgain = 5
        self.loot = 1.25
        self.mC = 1  # multiplier crit
        self.cR = 0  # cooldown R
        self.dealt = 0
        self.mR = 1  # multiplier R
        self.life = self.lifebase


class zombie:
    def __init__(self):
        self.life = 25
        self.damage = 5
        self.burn = 0


player = mage()
enemy = zombie()


def Q():  # funcoes das habilidades usadas pelo jogador
    player.life -= enemy.damage
    enemy.life -= player.damage * player.mR * player.mC


def W():
    player.life += player.lifebase * 0.4 * player.mR * player.mC
    if player.life > player.lifebase:
        player.life = player.lifebase


def E():
    player.life -= enemy.damage
    enemy.life -= player.damage * 0.8 * player.mR * player.mC
    enemy.burn = 4


def level_check():  # define a dificuldade do inimigo baseado na vida do jogador
    if player.level < 3:
        enemy.life = random.randint(15, 35)
        enemy.damage = 5
        player.XPgain = 5
        player.loot = 1.25
    elif player.level < 5:
        enemy.life = random.randint(50, 100)
        enemy.damage = 12
        player.XPgain = 7
        player.loot = 1.75
    elif player.level < 10:
        enemy.life = random.randint(100, 150)
        enemy.damage = 15
        player.XPgain = 8
        player.loot = 2.5
    else:
        enemy.life = random.randint(150, 250)
        enemy.damage = 20
        player.XPgain = 10
        player.loot = 3.25


def looplevelup():  # funcao para checar se o jogador subiu de nivel
    clear()
    print('\nXP: {}'.format(player.XP))
    if player.XP >= 10:
        player.level += 1
        player.XP -= 10

        print('level up! Current level: {}'.format(player.level))
        levelup = str(input('>>>increase total life by 8[L]\n>>>increase up base damage by 2[D]\n')).lower()
        if levelup == 'l':
            player.lifebase += 10
        elif levelup == 'd':
            player.damage = (player.damage / player.damagebase * (player.damagebase + 4))
            player.damagebase += 4
        else:
            print('\33[;31minsert valid option\33[m\n')
            looplevelup()
            player.level -= 1
            player.XP += 10


def loopdrop():  # funcao para a geracao e a escolha do item ganho ao matar o inimigo
    clear()
    drop = random.randint(1, 2)  # drop de espada ou armadura
    random1 = random.uniform(1, player.loot)
    if drop == 1:
        print("you've found a sword with a {:.2f}x damage multiplier".format(random1))
        print('your current one has a {:.2f}x damage multiplier'.format(player.damage / player.damagebase))
        change = str(input('would you like to change swords? \33[;32m[y]\33[m\33[;31m[n]\33[m '))
        if change == 'y':
            player.damage = player.damagebase * random1
        elif change == 'n':
            print("you're good to go")
        else:
            print('\33[;31minsert valid option\33[m\n')
            loopdrop()

    else:
        print("you've found a armor with a {:.2f}x armor multiplier".format(random1))
        print('your current one has a {:.2f}x armor multiplier'.format(player.armor / player.armorbase))
        change = str(input('would you like to change armors? \33[;32m[y]\33[m\33[;31m[n]\33[m '))
        if change == 'y':
            player.armor = player.armorbase * random1
        elif change == 'n':
            print("you're good to go")
        else:
            print('\33[;31minsert valid option\33[m\n')
            loopdrop()


def tela():  # printa na tela as informacoes da batalha
    clear()
    print('-' * 30)

    print('your health: ', end='')
    if player.life <= player.lifebase * 0.25:
        print('\33[;31m{:.2f}\33[m'.format(player.life))
    else:
        print('{:.2f}'.format(player.life))

    print('enemy health: {:.2f}\n'.format(enemy.life))

    print('>>>launch magic missile [Q]')
    print('>>>use heal [W]')

    if player.level >= 3:  # apenas desbloqueia apos o nivel 3
        print('>>>launch fireball [E]')

    if player.level >= 5:  # apenas desbloqueia apos o nivel 5
        print('>>>Ultimate [R]')

    print('-' * 30)


def battlefield():  # loop da batalha
    while player.life > 0:  # battlefield
        tela()
        if enemy.burn > 0:
            enemy.burn -= 1
            enemy.life -= player.damage * 0.2
        attack = str(input('hability: ')).upper()

        player.mC = 1

        if player.cR > 0:
            player.cR -= 1

        crit = random.randint(1, 10)
        if crit < 5:  # 50% de dar dano critico
            player.mC = 2
            if attack in ['Q', 'W', 'E']:
                print('crit!')

        if attack == 'Q':
            Q()
        elif attack == 'W':
            W()
        elif attack == 'E' and player.level >= 3:
            E()

        elif attack == 'R' and player.level >= 5 and player.cR == 0:
           player.mR = 2
           player.cR = 2

        else:
            print('\33[;31minsert valid option\33[m\n')

        if attack in ['q', 'w', 'e']:
            player.mR = 1

        if player.life <= 0:
            print('\n\33[;31myou died\33[m')
            sleep(3)
            exit()
        if enemy.life <= 0.01:
            player.XP += player.XPgain
            print(f'you killed him! \33[;32m+{player.XPgain}XP\33[m\n')
            break


def clear():  # limpa o console
    system('cls')


clear()
print("you wake on a farm, somehow you are still alive, you don't know what happened but")  # inicia o jogo com uma historia
print("you know that staying there won't be of any help\n")
print("\33[0;33m>>you are currently on the farm, press [ENTER] to begin<<\33[m\n")
input()


game_over = False
while not game_over:  # main loop
    clear()
    battlefield()
    loopdrop()
    level_check()
    looplevelup()
    player.life = player.lifebase
    print("\33[0;33msearching for monsters\33[m", end='')
    sleep(0.5)
    print("\33[0;33m.\33[m", end='')
    sleep(0.5)
    print("\33[0;33m.\33[m", end='')
    sleep(0.5)
    print("\33[0;33m.\33[m")
    sleep(0.5)
