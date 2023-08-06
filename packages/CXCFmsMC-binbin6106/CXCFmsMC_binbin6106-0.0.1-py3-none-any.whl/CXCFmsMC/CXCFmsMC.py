#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/10 9:30
# @Author  : UJN.Wenbin
# @FileName: CXCFmsMC.py
# @Software: PyCharm

from socket import *


class CXCFmsMC:
    def __init__(self, host):
        self.__host = host
        self.__port = 6500
        self.__buffSize = 2048
        self.__socketAddr = (self.__host, self.__port)
        self.__sendHeader = '500000FFFF0300'
        self.__resultStatus = {
            '0': 'Ok',
            1: 'Error',
            2: 'Not supported length',
            3: 'Not supported start address',
            4: 'Error var type'
        }
        self.__mcProtocolCmd = {
            # 批量读
            'batchReadCmd': '0104',
            'batchReadBitSubCmd': '0100',
            'batchReadBitWordSubCmd': '0000',
            # 批量写
            'batchWriteCmd': '0114',
            'batchWriteBitSubCmd': '0100',
            'batchWriteBitWordSubCmd': '0100',
        }
        self.__varCode = {
            # 软元件代码
            'X': '9C',
            'Y': '9D',
            'M': '90',
            'D': 'A8'
        }
        self.__cpuMonitorTimer = '1000'

    # varType: 0:inputRelay 1:outRelay 2:auxiliaryRelay 3:DataRegister
    def readBitFromPLC(self, startAddr, varType, length):
        if startAddr < 0 or startAddr > 65535:
            return self.__resultStatus[3]
        if length > 32:
            return self.__resultStatus[2]
        if length < 16:
            lengthStr = '0' + hex(length).lstrip('0x')
        else:
            lengthStr = hex(length).lstrip('0x')
        if varType == 'DataRegister':
            return self.__resultStatus[4]

        sendTail = self.__cpuMonitorTimer + \
                   self.__mcProtocolCmd['batchReadCmd'] + \
                   self.__mcProtocolCmd['batchReadBitSubCmd'] + \
                   self.__addrConvert(startAddr) + \
                   self.__varCode[varType] + \
                   lengthStr + '00'

        requestLength = hex(int(len(sendTail) / 2)).lstrip('0x') + '00'
        if len(requestLength) < 4:
            requestLength = '0' + requestLength

        sendStr = self.__sendHeader + requestLength + sendTail
        print(sendStr)
        return self.__dataProgress(startAddr, varType, length, self.__requesToPLC(bytes.fromhex(sendStr)))


    def __addrConvert(self, startAddr):
        if startAddr < 16:
            startAddr = '0' + hex(startAddr).lstrip('0x') + '0000'
        else:
            highStartAddr = hex(startAddr >> 8).lstrip('0x')
            if highStartAddr == '':
                highStartAddr = '00'
            if len(highStartAddr) < 2:
                highStartAddr = '0' + highStartAddr
            lowStartAddr = hex(startAddr).lstrip('0x')
            if len(lowStartAddr) < 2:
                lowStartAddr = '0' + lowStartAddr
            else:
                lowStartAddr = lowStartAddr[-2:]
            startAddr = lowStartAddr + highStartAddr + '00'
        return startAddr.upper()

    def __requesToPLC(self, sendBytes):
        tcpClient = socket(AF_INET, SOCK_STREAM)
        tcpClient.connect(self.__socketAddr)
        tcpClient.send(sendBytes)
        data = tcpClient.recv(self.__buffSize)
        sec = 2
        # res = [data[i:i+sec] for i in range(0, len(data), sec)]
        tcpClient.close()
        return data[11:]

    def __dataProgress(self, startAddr, varType, length, plcResult):
        aa = {}
        for i in range(length):
            aa[varType + str(startAddr + i)] = plcResult.hex()[i]
        return aa


if __name__ == '__main__':
    mc = CXCFmsMC('10.0.1.236')
    print(mc.readBitFromPLC(200, 'M', 5))

