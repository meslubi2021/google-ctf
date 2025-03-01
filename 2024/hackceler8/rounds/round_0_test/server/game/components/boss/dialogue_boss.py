# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from game.components.boss.boss import Boss
from game.engine import hitbox


class DialogueBoss(Boss):

    def __init__(self, coords):
        super().__init__(coords, name="dialogue_boss", tileset_path="resources/villain/snake_lady.h8t")
        self.name = "dialogue_boss"
        rect = hitbox.Rectangle(coords.x - 60, coords.x + 60, coords.y - 90, coords.y + 90)
        self.update_hitbox(rect)


    def _chat(self):
        if self.game.is_server or self.game.net is None:
            self.secret_server_dialogue()
        else:
            self.game.display_textbox(from_server=True, response_callbacks={"Imposssssible, that's correct": self._start_destruct})

    def secret_server_dialogue(self):
        # TODO BEFORE RELEASING TO PLAYERS: Remove block start
        def guess(resp: str):
            if resp.lower() == "hunter2":
                self.game.display_textbox("Imposssssible, that's correct!\n", process_fun=self._start_destruct)
            else:
                self.game.display_textbox("Incorrect! The correct answer is \"hunter2\".")

        def maybe_guess(resp: str):
            if resp == "I know the secret spell!":
                self.game.display_textbox("Let me hear it then!", free_text=True, process_fun=guess)
            else:
                self.game.display_textbox("Farewell")

        self.game.display_textbox("Greetingssss, mortal!\nYou shall not passss unless you can utter the secret sssspell.", choices=["I know the secret spell!", "Okay, bye"], process_fun=maybe_guess)
        return
        # TODO BEFORE RELEASING TO PLAYERS: Remove block end
        self.game.display_textbox("Boss battle only available on the sssserver.")

    def _start_destruct(self, text):
        text = "I've been defeated! Victory is yours young canine."
        self.sprite.set_animation("die")
        self.game.display_textbox(text, process_fun=self.destruct)

    def tick(self):
        super().tick()
        if self.destructing or self.dead:
            return
        self.sprite.set_flipped(self.game.player.x < self.x)
