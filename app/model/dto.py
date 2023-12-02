from model.model import Media
import json

class MediaDTO:
    media: Media

    def __init__(self, media) -> None:
        self.media = media

    def to_dict(self):
        media_dict = json.loads(self.media.to_json())
        media_dict.pop("src")
        media_dict.pop("_id")
        media_dict["timeWatched"] = self.media.timeWatched

        return media_dict