import axios from 'axios';

const styles = {
    buttonResult: {
    },
    buttonClear: {
    },
}

export const Form = (props) => {
    const handleResult = () => {
        let message = document.getElementById("message").value;

        if(message !== undefined && message !== "") {
            axios.get(`/prediction/${encodeURIComponent(message)}`)
            .then((res) => {
                return res.data
            })
            .catch((err) => {
                console.log(err)
            })
            .then((jsonRes) => {
                props.hookResult(jsonRes)
            })
        } else {
            props.hookResult({'prediction':''})
        }
    }

    const handleClear = () => {
        props.hookResult({'prediction':''})
        document.getElementById("message").value = "";
    }

    return(
        <div>
            <input type="text" placeholder="Enter your text..." id="message" name="message" autoFocus required />
            <input type="button" id="buttonResult" name="buttonResult" value="Result" style={styles.buttonResult} onClick={handleResult} />
            <input type="button" id="buttonClear" name="buttonClear" value="Clear" style={styles.buttonClear} onClick={handleClear} />
        </div>
    )
}