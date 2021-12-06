

model_name="MyChatBot"
rasa data validate && rasa train --fixed-model-name $model_name && rasa shell --model $model_name
