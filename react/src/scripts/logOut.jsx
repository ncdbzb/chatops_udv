import React from 'react';
import {RequestUserInformation} from './userInformation';

export function LogoutComponent(){
    // const {setIsLoggedIn} = RequestUserInformation();
    
    const logout = async () => {
    try {
        // Отправка запроса на выход пользователя
        const response = await fetch('https://f20a-5-165-8-39.ngrok-free.app/auth/logout', {
            method: 'POST',
            credentials: 'include', // Убедитесь, что куки прикрепляются к запросу
        });

        // Проверка успешности выполнения запроса на выход
        if (response.ok) {
            // setIsLoggedIn(false);

            console.log('User logged out successfully');
            // Выполните здесь необходимые действия после выхода пользователя (например, перенаправление на страницу входа)
        } else {
            console.error('Logout request failed');
        }
        } catch (error) {
            console.error('Logout error:', error);
        }
    }
    logout();
}
