 if  start_time == 0:
                    start_time = time.time()
                    
                else:  
                    current_time = time.time() #Retorna o tempo em segundos desde a era, mas que fica atualizando a cada loop
                    
                    #Cálculo para calcular o tempo decorrido desde que os olhos se fecharam
                    if current_time - start_time >= alarm_duration:
                        play.play_sound("sound/alarm.mp3")
                        start_time  = 0
