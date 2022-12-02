import admindb.settings
import engineer.settings
import researcher.settings
import repairman.settings
import fitter.settings

""" Для подключения нового приложения определите APP_RANK в settings.py приложения"""
RANK_PERSON = (
            (admindb.settings.APP_RANK, 'Админ базы данных'),
            (engineer.settings.APP_RANK, 'Инженер'),
            (repairman.settings.APP_RANK, 'Техник'),
            (researcher.settings.APP_RANK, 'Обследовальщик'),
            (fitter.settings.APP_RANK, 'Монтажник')
            )

""" Переменная для перенаправленя User согласно его rank"""
RANK_APP = {
            admindb.settings.APP_RANK:'admindb:profile',
            engineer.settings.APP_RANK:'engineer:profile',
            repairman.settings.APP_RANK:'repairman:profile',
            researcher.settings.APP_RANK:'researcher:profile',
            fitter.settings.APP_RANK:'fitter:profile',
            }

