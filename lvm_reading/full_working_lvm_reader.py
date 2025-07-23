import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
arquivo_temp = r"C:\Users\sinmec\Documents\HCSBS\LabView_TempXpwm\PWM\lvm_files\temp_info\temp_info.lvm"
arquivo_pwm = r"C:\Users\sinmec\Documents\HCSBS\LabView_TempXpwm\PWM\lvm_files\pwm_info\pwm_info.lvm"
arquivo_setpoint = r"C:\Users\sinmec\Documents\HCSBS\LabView_TempXpwm\PWM\lvm_files\setpoint_info\setpoint_info.lvm"

temp = pd.read_csv(arquivo_temp, delimiter="\t", skiprows=21, header=0, decimal=",")
pwm = pd.read_csv(arquivo_pwm, delimiter="\t", skiprows=21, header=0, decimal=",")
setpoint = pd.read_csv(arquivo_setpoint, delimiter="\t", skiprows=21, header=0, decimal=",")

# Excluindo coluna "Comment"
temp = temp.drop("Comment", axis=1)
pwm = pwm.drop("Comment", axis=1)
setpoint = setpoint.drop("Comment", axis=1)

# Padronização do tipo das variaveis e excluindo coluna "comment"
# temp["X_Value"] = temp["X_Value"].str.replace(",", ".").astype(float)
# temp["Untitled"] = temp["Untitled"].str.replace(",", ".").astype(float)
# temp = temp.drop("Comment", axis=1)
#
# pwm["X_Value"] = pwm["X_Value"].str.replace(",", ".").astype(float)
# pwm["Untitled"] = pwm["Untitled"].str.replace(",", ".").astype(float)
# pwm = pwm.drop("Comment", axis=1)
#
# setpoint["X_Value"] = setpoint["X_Value"].str.replace(",", ".").astype(float)
# setpoint["Untitled"] = setpoint["Untitled"].str.replace(",", ".").astype(float)
# setpoint = setpoint.drop("Comment", axis=1)

temp = temp.rename(columns={'X_Value':'Time'})
temp = temp.rename(columns={'Untitled':'Temperature'})
pwm = pwm.rename(columns={'X_Value':'Time'})
pwm = pwm.rename(columns={'Untitled':'pwm_output'})
setpoint = setpoint.rename(columns={'X_Value':'Time'})
setpoint = setpoint.rename(columns={'Untitled':'setpoint'})

pwm["pwm%"] = (pwm["pwm_output"]) / 250
pwm["Potência"] = (pwm["pwm%"]) * 240

# tempo_medio = (temp["Time"] + pwm["Time"]) / 2
tempo_medio = (temp["Time"] + pwm["Time"] + setpoint["Time"]) / 3

# Junta os DataFrames e adiciona a nova coluna
temp = temp.drop(columns=["Time"])
pwm = pwm.drop(columns=["Time"])
setpoint = setpoint.drop(columns=["Time"])

info = temp.join(pwm, how="outer")
info = info.join(setpoint, how="outer")


# Adiciona a nova coluna "Time" com a média
info["Time"] = tempo_medio

# Cria a figura e os dois eixos
fig, ax1 = plt.subplots(figsize=(10, 6))

# Eixo da esquerda - Temperatura
ax1.set_xlabel("Tempo (s)")
ax1.set_ylabel("Temperatura (°C)", color="red")
ax1.plot(info["Time"], info["Temperature"], color="red", label="Temperatura")
ax1.plot(info["Time"], info["setpoint"], color="green", linestyle="--", label="Setpoint")
ax1.tick_params(axis='y', labelcolor='red')

ax1.yaxis.set_major_locator(MultipleLocator(5))
ax1.yaxis.set_minor_locator(MultipleLocator(1))
ax1.grid(True, which='major', linestyle='-', linewidth=1)
ax1.grid(True, which='minor', linestyle='--', linewidth=0.5)

# Eixo da direita - PWM
# ax2 = ax1.twinx()
# ax2.set_ylabel("Potência (W)", color="blue")
# ax2.plot(info["Time"], info["Potência"], color="blue", label="Potência (W)")
# ax2.tick_params(axis='y', labelcolor='blue')

# Título e layout
plt.title("Temperatura e setpoint no Tempo")
fig.tight_layout()
plt.show()
