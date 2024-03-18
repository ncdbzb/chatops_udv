import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import styles from './test.css'
import Scripts from './scriptCreateTest'

const FormComponent = () => {
  const [file, setFile] = useState(null);
  const [numQuestions, setNumQuestions] = useState('');
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleNumQuestionsChange = (e) => {
    setNumQuestions(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('numQuestions', numQuestions);

    try {
      const response = await axios.post('http://127.0.0.1:8000', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }

return (
    <section className={styles.form}>
        <Link to="/">UDD LLMS </Link>
        <form action="/process_file" method="post" enctype="multipart/form-data" onSubmit={handleSubmit}>
          <p class="form-title"> Введите текст или добавьте файл с Вашего устройства </p>
          <div class="form-text-generation">
            <textarea name="text-generation" placeholder="Текст для генерации"></textarea>
          </div>
          <div class="container-doc">
            <input type="text" name="text-number-of-questions" placeholder="Количество вопросов" onChange={handleNumQuestionsChange} a/>
            <div class="input-file">
              <input type="file" name="file" accept=".docx, .doc, .pdf, .txt, .zip" onChange={handleFileChange} />
              <label for="file"><span> Выберите файл </span> </label>
            </div>  
          </div>
          
          <div class="text-questions">
            <input type="submit" name="send" value="Создать тест" />
          </div> 
        </form>
        <div id="gen_que_output"></div>
        <script scr={Scripts}></script>
    </section>        
)
}
export default FormComponent