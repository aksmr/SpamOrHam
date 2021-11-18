const styles = {
    footer: {
        fontSize: `calc(5px + 3vmin)`,
    },
    link: {
        textDecoration: "none",
        color:'black',
        fontWeight:'bold',
    },
}

export const Copyright = () => {
    return(
        <div style={styles.footer}>
            <small><a href="https://github.com/aksmr" style={styles.link}>AK47</a> © {new Date().getFullYear()}</small>
        </div>
    )
}