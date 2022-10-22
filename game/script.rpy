init -2 python:
    class Player:
        def __init__(self,x,y,xmin,ymin,xmax,ymax):
            self.x,self.y,self.xmin,self.ymin,self.xmax,self.ymax=x,y,xmin,ymin,xmax,ymax
            self.xoffset,self.yoffset=0,0
            self.won = False
            self.dead = False
            return
        def transform(self,d,show_time,animate_time):
            if self.dead:
                return 0
            self.x+=self.xoffset
            self.y+=self.yoffset
            self.xoffset,self.yoffset=0,0
            if self.x<self.xmin:
                self.x=self.xmin
            if self.y<self.ymin:
                self.y=self.ymin
            if self.x>self.xmax:
                self.x=self.xmax
            if self.y>self.ymax:
                self.y=self.ymax
            d.pos=(self.x,self.y)
            return 0
    class Arena:
        def __init__(self,player,*objects):
            self.player = player
            self.objects = objects
        def transform(self,d,show_time,animate_time):
            plr = self.player
            for obj in self.objects:
                dist = ((obj.x - plr.x)**2 + (obj.y - plr.y) ** 2)
                if dist < 0.05:
                    if type(obj) in (Trigger, Enemy):
                        obj.stepped_by(player)
    class Enemy:
        def __init__(self,x,y,nemesis):
            self.x = x
            self.y = y
            self.nemesis = nemesis
        def stepped_by(self,obj):
            obj.won = False
            obj.dead = True
        def transform(self,d,show_time,animate_time):
            x = self.x - self.nemesis.x
            y = self.y - self.nemesis.y
            step = 0.01
            if x:
                self.x -= step * x/abs(x)
            if y:
                self.y -= step * y/abs(y)

            d.pos=(self.x,self.y)

    class Trigger:
        def __init__(self,x,y,target, active=True):
            self.x = x
            self.y = y
            self.target = target
            self.active = active
        def stepped_by(self,obj):
            if self.active:
                self.target.activate()
            self.active=False
        def transform(self,d,show_time,animate_time):
            if self.active:
                d.pos=(self.x,self.y)
            else:
                d.pos=(-1.0,-1.0)
        def activate(self):
            self.active = True

    class Banner:
        def __init__(self,x,y,player):
            self.player = player
            self.banner_x, self.banner_y = x,y
            self.x,self.y=-1.0,-1.0
        def transform(self,d,show_time,animate_time):
            d.pos=(self.x,self.y)
        def activate(self):
            self.player.won = True
            self.x,self.y = self.banner_x,self.banner_y


    player=Player(0.5,0.5,0.05,0.05,0.95,0.95)
    winning_banner = Banner(0.1,0.1, player)
    exit_trigger = Trigger(0.9,0.1, winning_banner,active=False)
    control_trigger = Trigger(0.8,0.8,exit_trigger)
    shroom = Enemy(0.2,0.2,player)
    main_arena = Arena(player,
                       winning_banner,
                       exit_trigger,
                       control_trigger,
                       shroom,
                       )

screen hamster_cage:

    add "bg field" at Transform(function=main_arena.transform)

    add "banner"at Transform(function=winning_banner.transform)
    add "target"at Transform(function=control_trigger.transform)
    add "target"at Transform(function=exit_trigger.transform)
    add "potato happy" anchor (0.5,0.5) at Transform(function=player.transform)
    add "shroom hunter" at Transform(function=shroom.transform)

    key "focus_left" action SetField(player,"xoffset",-0.05)
    key "focus_right" action SetField(player,"xoffset",+0.05)
    key "focus_up" action SetField(player,"yoffset",-0.05)
    key "focus_down" action SetField(player,"yoffset",+0.05)
    key "dismiss" action Return("hamster")


define e = Character('мисс картошка', color="#000000")

transform left_center: #позиция гдето слева по центру
    xalign 0.3 yalign 0.2

transform left_move_in: #позиция гдето слева по центру
    xalign -1 yalign 0.2
    linear 1 xalign 0.3


transform left_jumping: #позиция гдето слева по центру
    xalign 0.3 yalign 0.2
    linear 0.5 yalign 0.4
    linear 0.5 yalign 0.2
    repeat

label start:
    call screen hamster_cage
    if not player.won:
        jump game_over

    scene bg field
    e "нет картошки"

    show potato happy at left_move_in

    e "КАРТОШКА"
    show potato happy at left_center
    menu:
        "картошка? или не картошка?"
        "что такое картошка?":
            e "картошка?"
            show potato happy at left_jumping
            e   """КАРТОШКА\n
                картошка\n
                клубнеплод\n"""
        "картошка":
            show potato princess at left_jumping
            e "урааа"
        "не картошка":
            jump game_over

    return
label game_over:
    scene bg fail
    "вы хорошо цеплялись за комья земли на пути к солнечному свету"
    "на правда жизни такова что всходят не все посевы"
    menu:
        "начать заново?"
        "да":
            jump start
        "нет":
            "редиски ответ"
