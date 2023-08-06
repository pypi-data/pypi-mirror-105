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
            0: 'Ok',
            1: 'Error',
            2: 'Not supported length',
            3: 'Not supported start address',
            4: 'Error var type',
            5: 'Error data length',
            6: 'Data length not equal',
            7: 'Error PLC response'
        }
        self.__mcProtocolCmd = {
            # 批量读
            'batchReadCmd': '0104',
            'batchReadBitSubCmd': '0100',
            'batchReadWordSubCmd': '0000',
            # 批量写
            'batchWriteCmd': '0114',
            'batchWriteBitSubCmd': '0100',
            'batchWriteWordSubCmd': '0000',
        }
        self.__varCode = {
            # 软元件代码
            'X': '9C',
            'Y': '9D',
            'M': '90',
            'D': 'A8'
        }
        self.__cpuMonitorTimer = '1000'

    def readBitFromPLC(self, startAddr, varType, length):
        if startAddr < 0 or startAddr > 65535:
            return self.__resultStatus[3]
        if length > 32:
            return self.__resultStatus[2]
        if length < 16:
            lengthStr = '0' + hex(length).lstrip('0x')
        else:
            lengthStr = hex(length).lstrip('0x')
        if varType == 'D':
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
        # return sendStr
        return self.__dataProgress(startAddr, varType, length, self.__requesToPLC(bytes.fromhex(sendStr.upper())))

    def readWordFromPLC(self, startAddr, varType, length):
        if startAddr < 0 or startAddr > 65535:
            return self.__resultStatus[3]
        if length > 32:
            return self.__resultStatus[2]
        if length < 16:
            lengthStr = '0' + hex(length).lstrip('0x')
        else:
            lengthStr = hex(length).lstrip('0x')
        if varType == 'M':
            return self.__resultStatus[4]

        sendTail = self.__cpuMonitorTimer + \
                   self.__mcProtocolCmd['batchReadCmd'] + \
                   self.__mcProtocolCmd['batchReadWordSubCmd'] + \
                   self.__addrConvert(startAddr) + \
                   self.__varCode[varType] + \
                   lengthStr + '00'

        requestLength = hex(int(len(sendTail) / 2)).lstrip('0x') + '00'
        if len(requestLength) < 4:
            requestLength = '0' + requestLength

        sendStr = self.__sendHeader + requestLength + sendTail
        # return sendStr
        return self.__dataProgress(startAddr, varType, length, self.__requesToPLC(bytes.fromhex(sendStr.upper())))

    def writeBiToPLC(self, startAddr, varType, length, data):
        if startAddr < 0 or startAddr > 65535:
            return self.__resultStatus[3]
        if length > 32:
            return self.__resultStatus[2]
        if length < 16:
            lengthStr = '0' + hex(length).lstrip('0x')
        else:
            lengthStr = hex(length).lstrip('0x')
        if varType == 'D':
            return self.__resultStatus[4]
        if len(data) % 2 != 0:
            return self.__resultStatus[5]
        if len(data) != length:
            return self.__resultStatus[6]

        sendTail = self.__cpuMonitorTimer + \
                   self.__mcProtocolCmd['batchWriteCmd'] + \
                   self.__mcProtocolCmd['batchWriteBitSubCmd'] + \
                   self.__addrConvert(startAddr) + \
                   self.__varCode[varType] + lengthStr + '00' + data

        requestLength = hex(int(len(sendTail) / 2)).lstrip('0x') + '00'
        if len(requestLength) < 4:
            requestLength = '0' + requestLength

        sendStr = self.__sendHeader + requestLength + sendTail
        # return sendStr
        return self.__dataProgress(startAddr, varType, length, self.__requesToPLC(bytes.fromhex(sendStr.upper())))

    def writeWordToPLC(self, startAddr, varType, length, data):
        if startAddr < 0 or startAddr > 65535:
            return self.__resultStatus[3]
        if length > 32:
            return self.__resultStatus[2]
        if length < 16:
            lengthStr = '0' + hex(length).lstrip('0x')
        else:
            lengthStr = hex(length).lstrip('0x')
        if varType == 'M':
            return self.__resultStatus[4]
        if len(data) != length:
            return self.__resultStatus[6]
        progressData = ''
        for i in data:
            hexStr = hex(i).lstrip('0x').zfill(4)
            header = hexStr[:2]
            tail = hexStr[2:]
            hexStr = tail + header
            progressData += hexStr

        sendTail = self.__cpuMonitorTimer + \
                   self.__mcProtocolCmd['batchWriteCmd'] + \
                   self.__mcProtocolCmd['batchWriteWordSubCmd'] + \
                   self.__addrConvert(startAddr) + \
                   self.__varCode[varType] + lengthStr + '00' + progressData

        requestLength = hex(int(len(sendTail) / 2)).lstrip('0x') + '00'
        if len(requestLength) < 4:
            requestLength = '0' + requestLength

        sendStr = self.__sendHeader + requestLength + sendTail
        # return sendStr
        return self.__dataProgress(startAddr, varType, length, self.__requesToPLC(bytes.fromhex(sendStr.upper())))

    def __addrConvert(self, startAddr):
        if 0 < startAddr < 16:
            startAddr = '0' + hex(startAddr).lstrip('0x') + '0000'
        elif startAddr == 0:
            startAddr = '000000'
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
        try:
            tcpClient.connect(self.__socketAddr)
            tcpClient.send(sendBytes)
            data = tcpClient.recv(self.__buffSize)
            return data
        except ConnectionRefusedError:
            return self.__resultStatus[1] + ' reason: Ip or port error.'
        finally:
            tcpClient.close()

    def __dataProgress(self, startAddr, varType, length, plcResult):
        if isinstance(plcResult, str):
            return plcResult
        resCode = self.__checkResponseCode(plcResult)
        if resCode[0] == self.__resultStatus[0]:
            # read operation
            if resCode[1].hex() != '':
                if varType == 'M':
                    aa = {}
                    for i in range(length):
                        aa[varType + str(startAddr + i)] = resCode[1].hex()[i]
                    return aa
                elif varType == 'D':
                    aa = {}
                    tempList = []
                    i = 0
                    sec = 1
                    wordResList = [resCode[1][i:i + sec] for i in range(0, len(resCode[1]), sec)]
                    while i < len(wordResList):
                        tempList.append(int((wordResList[i + 1].hex() + wordResList[i].hex()), 16))
                        i += 2
                    for j in range(length):
                        aa[varType + str(startAddr + j)] = tempList[j]
                    return aa
            else:
                # write operation
                return self.__resultStatus[0]
        else:
            return self.__resultStatus[1]

    def __checkResponseCode(self, responseCode):
        header = responseCode[:11]
        tail = responseCode[11:]
        if header.hex()[-4:] != '0000':
            return self.__resultStatus[7]
        else:
            return [self.__resultStatus[0], tail]


if __name__ == '__main__':
    # test code
    mc = CXCFmsMC('10.0.1.236')
    # print(mc.readBitFromPLC(0, 'M', 16))
    # print(mc.readWordFromPLC(0, 'D', 6))
    # print(mc.writeBiToPLC(210, 'M', 8, '00000000'))
    # print(mc.writeWordToPLC(200, 'D', 3, [0, 0, 0]))
