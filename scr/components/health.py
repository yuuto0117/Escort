from . import component



class Health(component.Component):
    def __init__(self, owner, health=100, thoughness=20, recovery_rate=5):
        super().__init__(owner)

        self.health = health
        self.thoughness = thoughness
        # 最大体力值
        self.max_thoughness = thoughness
        self.recovery_rate = recovery_rate
        # 小计时器
        self.timer = 0
        # 状态
        self.alive = True
        # 受伤信号
        self.hurt = False
        # 防御成功
        self.defence_invincible_timer = 0
        self.is_defence_invincible = False

        # 无敌帧
        self.invincible_time = 28


    def hurt_check(self):
        # 受伤无敌帧
        if self.hurt:
            self.timer += 1
            if self.timer >= self.invincible_time:
                self.timer = 0
                self.hurt = False
        #  防御无敌帧
        if self.is_defence_invincible:
            self.defence_invincible_timer += 1
            if self.defence_invincible_timer >= self.invincible_time:
                self.is_defence_invincible = False
                self.defence_invincible_timer = 0


    def take_damage(self, damage):
        if self.is_defence_invincible:
            return

        self.health -= damage
        self.hurt = True


    def heal(self, amount):
        self.health += amount


    def defended(self, damage):
        # 韧性值够扣韧性值
        if self.thoughness > damage:
            self.thoughness -= damage
            # self.successed_defence = True
            self.is_defence_invincible = True
            self.defence_invincible_timer = 0
            return
        # 韧性值不足扣血
        else:
            self.health -= damage - self.thoughness
            self.thoughness = 0
            self.hurt = True


    def consume(self, amount):
        self.thoughness -= amount
        if self.thoughness < 0:
            self.thoughness = 0


    def update(self):
        # 检测受伤
        self.hurt_check()

        # 检查是否死亡
        if self.health <= 0:
            self.health = 0
            self.alive = False


        # 恢复韧性值
        self.timer += 1
        if self.timer >= 60:  # 每秒恢复1次
            self.timer = 0
            self.thoughness += self.recovery_rate
            if self.thoughness >= self.max_thoughness:
                self.thoughness = self.max_thoughness










