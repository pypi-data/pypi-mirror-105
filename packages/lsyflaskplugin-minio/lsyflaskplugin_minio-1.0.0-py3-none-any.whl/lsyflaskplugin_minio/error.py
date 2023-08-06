# -*- coding: utf-8 -*-


class MinioError(Exception):
    @property
    def message(self):
        return self.args[0]
