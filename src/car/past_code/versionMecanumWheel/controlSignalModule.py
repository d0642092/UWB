'''
尚未完成:
    1.乘法內部.....小數點 float
    2.加減法內部...減法
'''

# def oldcode():
    # multinum = (power_multi).to_bytes(1, byteorder='big', signed=True)
    # multinum_hex = int(multinum.hex(), base=16)
    #
    # print('multinum = ', end='')
    # print(multinum)
    # print('multinum_hex = ', end='')
    # print(multinum_hex)

    # if self.currentPower * multinum_hex <= 255:
    #     self.currentPower *= multinum_hex
    # else:
    #     return -1

class commandConvert():
    def __init__(self):
        self.cmd = b'\xFA\x08\x80\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A'
        self.currentPower = 128

    def showCmd(self):
        print(self.cmd)

    def cmdModify(self, cmd, direct, power_add, power_multi):
        self.currentPower = self.cmdgetCurrentPower(cmd, 2)
        # 功率乘法

        if self.currentPower * power_multi <= 255:
            self.currentPower *= power_multi
            self.currentPower = int(self.currentPower)
        else:
            return -1

        # 功率加法
        if 255 >= self.currentPower + power_add >= 0:
            self.currentPower += power_add
        else:
            return -1

        newpower = '0' + hex(self.currentPower).replace('0x', '', 1) if len(hex(self.currentPower)) < 2 else hex(self.currentPower).replace('0x', '', 1)
        self.cmd = bytes.fromhex(self.cmdsetCmdDirPower(cmd, direct, newpower))
        return 0

    def cmdgetCurrentPower(self, cmd, position):
        cmdList = list()
        strtmp = ''

        for i in cmd.hex():
            strtmp += i
            if len(strtmp) >= 2:
                cmdList.append(strtmp)
                strtmp = ''

        return int(cmdList[position], base=16)

    def cmdsetCmdDirPower(self, cmd, direct, newpower):
        cmdList = list()
        strtmp = ''

        # 修改指令第三個位址(功率部分)
        for i in cmd.hex():
            strtmp += i
            if len(strtmp) >= 2:
                cmdList.append(strtmp)
                strtmp = ''
        cmdList[1] = direct
        cmdList[2] = newpower

        # 組成指令
        strtmp = ''
        for i in cmdList:
            strtmp += i

        return strtmp


if __name__ == '__main__':
    modifyCmdTest = commandConvert()

    print(modifyCmdTest.cmd)

    print('Default Cmd: ', end='')
    print(b'\xFA\x08\x80\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')

    multi = 1
    add = 0

    while add != -888:
        multi = float(input('Multi Power:'))
        add = int(input('Add Power:'))

        if modifyCmdTest.cmdModify(b'\xFA\x08\x80\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A', '08', add, multi) != -1:
            modifyCmdTest.showCmd()
        else:
            print('Out of Power Limit')
