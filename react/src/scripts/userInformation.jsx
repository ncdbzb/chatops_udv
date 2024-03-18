import React, { useState, useEffect } from 'react';

export function RequestUserInformation(){
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userData, setUserData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        const userInformation = () =>{
            return(
                fetch('https://f20a-5-165-8-39.ngrok-free.app/users/me', {
                        method: 'GET',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json', // Установка Content-Type на application/json
                        },
                    }).then(response => {
                        if (!response.ok) {
                        throw new Error('Ошибка HTTP: ' + response.status);
                        }

                        setIsLoggedIn(true);
                        // Преобразование ответа в формат JSON
                        return response.json();
                    })
                    .then(data => {
                        // Обработка полученных данных
                        
                        // Здесь вы можете обновить состояние компонента или выполнить другие действия с полученными данными

                    })
                    .catch(error => {
                        // Обработка ошибок
                        console.error('Ошибка при выполнении запроса:', error);
                    })
                
            )
        }
        userInformation()
    })
}