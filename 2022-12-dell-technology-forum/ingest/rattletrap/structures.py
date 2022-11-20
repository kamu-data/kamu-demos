class ReplayHeader:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_json(json_data: dict) -> 'ReplayHeader':
        return ReplayHeader(json_data)
    # todo


class ReplayContent:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_json(json_data: dict) -> 'ReplayContent':
        return ReplayContent(json_data)
    # todo


class Replay:
    def __init__(self, header: 'ReplayHeader', content: 'ReplayContent'):
        self._header = header
        self._content = content

    @property
    def header(self) -> 'ReplayHeader':
        return self._header

    @property
    def content(self) -> 'ReplayContent':
        return self._content

    @staticmethod
    def from_json(json_data: dict) -> 'Replay':
        return Replay(
            ReplayHeader.from_json(json_data["header"]),
            ReplayContent.from_json(json_data["content"])
        )
