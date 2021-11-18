import {useState} from 'react';
import { Form } from './Components/Form';
import { Result } from './Components/Result';
import { Copyright } from './Components/Copyright';

const styles = {
    app: {
        textAlign: 'center',
        background: `linear-gradient(to right bottom, #f1e8b8, #caa791, #8e7071, #4d4349, #191919)`,
        height: '100vh',
    },
    title: {
        fontSize: `calc(10px + 7vmin)`,
        fontWeight: 'bold',
        marginBottom: '10vh',
    },
    explication: {
        fontSize: `calc(10px + 3vmin)`,
        padding:'3vh',
    },
}

export const App = () => {
    const [result, setResult] = useState({})

	return (
		<div style={styles.app}>
			<div style={styles.title}>Spam or Ham</div>
            <small style={styles.explication}>The application allows you to find out whether a previously entered text is considered spam or not...</small>
            <br /><br />
            <Form hookResult={setResult} />
            <br />
            <Result printResult={result} />
            <br /><br />
            <Copyright />
		</div>
	);
}