from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel, Field

from track_passport.application import constants


class LadleData(BaseModel):
    ladle_id: int = Field(description='ИД ковша')


class LadleTrackerData(BaseModel):
    id: int
    location: Optional[constants.Location] = None
    is_filled: Optional[bool] = None


class LadleTrackerInfo(BaseModel):
    id: int
    number: int
    location: Optional[str]
    time_in_location: str
    located_at: Optional[datetime]
    previous_location_left_at: Optional[datetime]
    in_work: bool
    is_filled: bool
    liner_temperature: float
    capacity: float
    collector_diameter: float
    collector_resistance: int
    ladle_resistance: int
    nesting_block_resistance: int
    ladle_turnaround_time: int
    metal_in_ladle_time: int
    bottom_tuyere_state: Optional[str]
    casting_direction: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'number': 12,
                'location': 'СБС3',
                'in_work': 'true',
                'is_filled': 'false',
                'liner_temperature': 451,
                'capacity': 25.6,
                'collector_diameter': 110.5,
                'collector_resistance': 192,
                'ladle_resistance': 168,
                'nesting_block_resistance': 0,
                'ladle_turnaround_time': 360,
                'metal_in_ladle_time': 144,
                'bottom_tuyere_state': 'NORMAL',
                'casting_direction': 'MOULD',
            }
        }


class SuccessMsg(BaseModel):
    success: bool

    class Config:
        schema_extra = {
            'example': {
                'success': True,
            }
        }


class LadleTrackers(BaseModel):
    __root__: Sequence[LadleTrackerInfo]
