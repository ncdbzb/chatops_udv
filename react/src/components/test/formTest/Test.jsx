import { Link } from 'react-router-dom';
import styles from './test.css'
import Scripts from './scriptCreateTest'

const Test = () =>{
    return (
        <section className={styles.form}>
            <Link to="/">UDD LLMS </Link>
            <form action="/process_file" method="post" enctype="multipart/form-data" >
              <p class="form-title"> Введите текст или добавьте файл с Вашего устройства </p>
              <div class="form-text-generation">
                <textarea name="text-generation" placeholder="Текст для генерации"></textarea>
              </div>
              <div class="container-doc">
                <input type="text" name="text-number-of-questions" placeholder="Количество вопросов" />
                <div class="input-file">
                  <input type="file" name="file" accept=".docx, .doc, .pdf, .txt, .zip" />
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
export default Test;