from pydantic import BaseModel


class AlarmModel(BaseModel):
    deviceCode: str
    companyCode: str
    lineCode: int
    alarmEventId: str
    alarmStatus: int
    alarmTime: str
    alarmType: int
    alarmId: str
    alarmLevel: str
    alarmSource: str
    position: str
    alarmImage: str
    cameraStartTime: str
    cameraEndTime: str
    cameraDeviceId: str
    cameraChannelId: str

    def get_status(self):
        statue_data = [0, "开始", "进行中", "结束"]
        return statue_data[self.alarmStatus]
