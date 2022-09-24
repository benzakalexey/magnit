from evraz.classic.components import component
from evraz.spectree import Response

from track_passport.adapters.http_api.join_points import join_point
from track_passport.adapters.http_api.spec import spectree
from track_passport.application.tracker import services

from .models.mnemonic_scheme import LadleTrackers, SuccessMsg, LadleData, \
    LadleTrackerInfo, LadleTrackerData


@component
class MnemonicScheme:
    service: services.Tracker

    @join_point
    @spectree.validate(resp=Response(HTTP_200=LadleTrackers))
    def on_get_get_data(self, request, response):
        trackers = self.service.get_trackers()

        response.media = [
            {
                'id': tracker.ladle.id,
                'number': tracker.ladle.number,
                'location': tracker.location.value
                if tracker.location else None,
                'time_in_location': (
                    f'{tracker.sec_in_location // 3600}:'
                    f'{tracker.sec_in_location % 3600 // 60}'
                ),
                'located_at': tracker.located_at,
                'previous_location_left_at': tracker.previous_location_left_at,
                'in_work': tracker.in_work,
                'is_filled': tracker.is_filled,
                'liner_temperature': tracker.liner_temperature,
                'capacity': tracker.capacity,
                'collector_diameter': tracker.collector_diameter,
                'collector_resistance': tracker.collector_resistance,
                'ladle_resistance': tracker.ladle_resistance,
                'nesting_block_resistance': tracker.nesting_block_resistance,
                'ladle_turnaround_time': tracker.ladle_turnaround_time,
                'metal_in_ladle_time': int(tracker.metal_in_ladle_time),
                'bottom_tuyere_state': tracker.bottom_tuyere_state.value
                if tracker.bottom_tuyere_state else None,
                'casting_direction': tracker.casting_direction.value
                if tracker.casting_direction else None,
            } for tracker in trackers
        ]

    @join_point
    @spectree.validate(
        query=LadleData, resp=Response(HTTP_200=LadleTrackerInfo)
    )
    def on_get_get_ladle_data(self, request, response):
        query: LadleData = request.context.query

        tracker = self.service.get_by_ladle_id(query.ladle_id)
        response.media = {
            'id': tracker.ladle.id,
            'number': tracker.ladle.number,
            'location': tracker.location.value if tracker.location else None,
            'time_in_location': (
                f'{tracker.sec_in_location // 3600}:'
                f'{tracker.sec_in_location % 3600 // 60}'
            ),
            'located_at': tracker.located_at,
            'previous_location_left_at': tracker.previous_location_left_at,
            'in_work': tracker.in_work,
            'is_filled': tracker.is_filled,
            'liner_temperature': tracker.liner_temperature,
            'capacity': tracker.capacity,
            'collector_diameter': tracker.collector_diameter,
            'collector_resistance': tracker.collector_resistance,
            'ladle_resistance': tracker.ladle_resistance,
            'nesting_block_resistance': tracker.nesting_block_resistance,
            'ladle_turnaround_time': tracker.ladle_turnaround_time,
            'metal_in_ladle_time': int(tracker.metal_in_ladle_time),
            'bottom_tuyere_state': tracker.bottom_tuyere_state.value
            if tracker.bottom_tuyere_state else None,
            'casting_direction': tracker.casting_direction.value
            if tracker.casting_direction else None,
        }

    @join_point
    @spectree.validate(
        json=LadleTrackerData, resp=Response(HTTP_200=SuccessMsg)
    )
    def on_post_update_ladle_data(self, request, response):
        json_body: LadleTrackerData = request.context.json

        self.service.update_tracker_data(**json_body.dict(exclude_none=True))

        msg = SuccessMsg(success=True)
        response.media = msg.dict()
