const styles = {
    link: {
        textDecoration: "none",
        color:'black',
        fontWeight:'bold',
    }
}

export const Copyright = () => {
    return(
        <div>
            <small><a href="https://github.com/aksmr" style={styles.link}>AK47</a> © {new Date().getFullYear()}</small>
        </div>
    )
}