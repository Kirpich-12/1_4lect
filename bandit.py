import tkinter as tk
import random

from casmath import get_finals

EMOJIS = ["🍒", "7️⃣", "🍋", "🔔", "🍀", "💎", "7️⃣", "7️⃣", "7️⃣"]
# выплаты для трёх одинаковых (коэффициент от ставки)
PAYOUTS = {
    "7️⃣": 50,
    "💎": 20,
    "🔔": 10,
    "🍒": 5,
    "🍋": 3,
    "🍀": 2,
}

class OneArmedBandit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Однорукий бандит — tkinter")
        self.resizable(False, False)
        self.credits = 100
        self.bet = 1
        self.is_spinning = False
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")
        self.geometry("500x300")

        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self, pady=10)
        top.pack()

        # Рамка с катушками
        reels_frame = tk.Frame(top)
        reels_frame.pack(padx=10, pady=5)

        self.reel_labels = []
        for i in range(3):
            lbl = tk.Label(reels_frame, text=random.choice(EMOJIS), font=("Segoe UI Emoji", 60), width=2)
            lbl.grid(row=0, column=i, padx=8)
            self.reel_labels.append(lbl)

        # Инфо и управление
        info = tk.Frame(self, pady=8)
        info.pack(fill="x")

        self.credits_var = tk.StringVar(value=f"Кредиты: {self.credits}")
        tk.Label(info, textvariable=self.credits_var, font=("Arial", 12)).pack(side="left", padx=8)

        tk.Label(info, text="Ставка:", font=("Arial", 12)).pack(side="left")
        self.bet_var = tk.IntVar(value=self.bet)
        bet_spin = tk.Spinbox(info, from_=1, to=50, width=4, textvariable=self.bet_var, command=self._on_bet_changed)
        bet_spin.pack(side="left", padx=6)

        self.spin_btn = tk.Button(info, text="СПИН", font=("Arial", 12, "bold"), command=self.spin, width=8)
        self.spin_btn.pack(side="right", padx=8)

        # Сообщения о результате
        self.message_var = tk.StringVar(value="Удачи!")
        tk.Label(self, textvariable=self.message_var, font=("Arial", 12)).pack(pady=(0,10))

        # Быстрые кнопки
        bottom = tk.Frame(self, pady=6)
        bottom.pack()
        tk.Button(bottom, text="Добавить 50 кредитов", command=self.add_credits).pack(side="left", padx=6)
        tk.Button(bottom, text="Сброс", command=self.reset).pack(side="left", padx=6)
        tk.Button(bottom, text="Выход", command=self.destroy).pack(side="left", padx=6)

    def _on_bet_changed(self):
        try:
            b = int(self.bet_var.get())
            if b < 1:
                b = 1
            self.bet = b
        except Exception:
            self.bet_var.set(self.bet)

    def add_credits(self):
        self.credits += 50
        self._update_credits_display()
        self.message_var.set("Кредиты пополнены +50")

    def reset(self):
        if self.is_spinning:
            return
        self.credits = 100
        self.bet = 1
        self.bet_var.set(1)
        self._update_credits_display()
        self.message_var.set("Игра сброшена.")

    def _update_credits_display(self):
        self.credits_var.set(f"Кредиты: {self.credits}")

    def spin(self):
        if self.is_spinning:
            return
        try:
            bet = int(self.bet_var.get())
        except Exception:
            bet = 1
            self.bet_var.set(1)

        if bet <= 0:
            self.message_var.set("Ставка должна быть >= 1")
            return
        if bet > self.credits:
            self.message_var.set("Недостаточно кредитов на ставку")
            return

        # Списываем ставку и начинаем крутить
        self.credits -= bet
        self._update_credits_display()
        self.message_var.set("Крутим...")
        self.spin_btn.config(state="disabled")
        self.is_spinning = True

        # продолжительности вращения для каждой катушки (мс)
        durations = [random.randint(80, 140), random.randint(120, 200), random.randint(160, 260)]
        start_time = self.after(0, lambda: None)  # placeholder
        self._start_time = self._now_ms()

        # создаём конечные результаты заранее (или можно случайно выбрать когда остановятся)
        # final = [random.choice(EMOJIS) for _ in range(3)]
        final = get_finals()
        
        self._spin_state = {
            "final": final,
            "durations": durations,
            "start_ms": self._now_ms()
        }
        # запускаем анимацию для каждой катушки
        for i in range(3):
            self._animate_reel(i)

    def _now_ms(self):
        return int(self.winfo_pointerx() or 0)  # not reliable for time; use after info alternative

    # альтернатива для тайминга — используем внутренний счётчик вызовов
    def _animate_reel(self, reel_index, ticks=0):
        # ticks — количество обновлений прошедших для этой катушки
        # чтобы упростить: будем считать по количеству шагов, а не абсолютным времени
        if not hasattr(self, "_ticks"):
            self._ticks = [0,0,0]
        self._ticks[reel_index] += 1
        t = self._ticks[reel_index]

        # быстрое обновление символа
        self.reel_labels[reel_index].config(text=random.choice(EMOJIS))

        # замедление: остановим после определённого числа шагов, зависящего от желаемой "длительности"
        # пересчитаем длительность в количестве тиков (примерно 20-60 тиков)
        dur_ms = self._spin_state["durations"][reel_index]
        max_ticks = max(6, dur_ms // 40)  # 40ms на тик приблизительно
        if t >= max_ticks:
            # ставим финальный символ
            final_symbol = self._spin_state["final"][reel_index]
            self.reel_labels[reel_index].config(text=final_symbol)
            # проверяем, остановились ли все
            if all(self._ticks[i] >= max(6, self._spin_state["durations"][i] // 40) for i in range(3)):
                self.after(200, self._on_spin_finished)
            return
        # иначе продолжить крутить — с небольшой задержкой, делаем эффект замедления
        delay = 30 + int((t / max_ticks) * 80)  # от 30 до ~110 ms
        self.after(delay, lambda: self._animate_reel(reel_index, t+1))

    def _on_spin_finished(self):
        self.is_spinning = False
        self.spin_btn.config(state="normal")
        # сбросим счётчики тиков для следующего круга
        if hasattr(self, "_ticks"):
            self._ticks = [0,0,0]
        result = [lbl.cget("text") for lbl in self.reel_labels]
        self._evaluate_result(result)

    def _evaluate_result(self, result):
        # простой подсчёт: если три одинаковых — большая выплата, если две — мелкая
        msg = "Результат: " + " ".join(result)
        if result[0] == result[1] == result[2]:
            sym = result[0]
            multiplier = PAYOUTS.get(sym, 1)
            win = self.bet * multiplier
            self.credits += win
            self._update_credits_display()
            self.message_var.set(f"{msg} — ВЫИГРАЛИ {win} (x{multiplier})!")
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            # парная выплата — 1.5x ставки (округляем вниз)
            win = int(self.bet * 1.5)
            self.credits += win
            self._update_credits_display()
            self.message_var.set(f"{msg} — ПАРА! Выигрыш {win}.")
        else:
            self.message_var.set(f"{msg} — Увы, ничего. Попробуйте ещё.")

if __name__ == "__main__":
    app = OneArmedBandit()
    app.mainloop()
