const styles = {
    result: {
        fontSize: `calc(20px + 6vmin)`,
        margin: '3vh',
        color: '#DEDEDE',
    }
}

export const Result = (props) => {
    return(
        <div id="result" name="result" style={styles.result}>
            {props.printResult.prediction !== undefined && props.printResult.prediction !== ""  ? `This is a ${props.printResult.prediction.toUpperCase()}!` : ``}
        </div>
    )
}