# mf_HSE_match_front_bot
Registration form for Matching Bot for matfak.


**Вы можете отправить заявку на предарительное тестирование или добавление функционала**

Первокурсникам на матфаке не хватает совета старших товарищей.
С этим борются кураторы и учебные ассистенты.

Я предлагаю в начале сентября немного времени потратить на то, чтобы познакомить 
старшекурсников и младшекурсников друг с другом.

Для этого в начале сентября я хочу запустить вот этого бота, который соберёт
заявки от желающих старше- и младшекурсников, и выдаст контакты по принципу
регулярного двудольного графа с степенью вершин 2 и одним циклом, где в одной
доле старшекурсники, а в другой младшекурсники.

**UPD**

Решила добавить второкурсников в отдельную когорту, в зависимости от количества желающих мы смэтчим их либо  с чуваками старше, либо младше,
 либо и старше, и младше.
 
__Количество людей будет неравное, так что надо будет подумать отдельно, как лучше раздать контакты.__

Совмещение будет либо вручную, либо с помощью отдельной программы на питоне.

Бот отправляет отладочную информацию в группу, чтобы я могла следить за процессом регистрации,
каждая успешная регистрация вызывает дамп базы данных в бинарный файл, хранящий
питоновский словарь. Резервные копии дампа создаются раз в день.

Проект хостится на pythonAnywhere.com

Ориентировочное время работы бота 14-20 сентября 2020
