import React from 'react';
import axios from 'axios';
import {Button, TextField, Grid} from '@mui/material';
import { styled } from '@mui/material/styles';

const styles = {
    buttonResult: {
        cursor: 'pointer',
    },
    buttonClear: {
        cursor: 'pointer',
    },
    form: {
        marginTop: '4vh',
        padding: '0vh 9vh 0vh 9vh',
    },
}

const ResultButton = styled(Button)(({ theme }) => ({
    color: theme.palette.getContrastText('#000000'),
    fontFamily: `Shadows Into Light, cursive`,
    backgroundColor: '#343a40',
    borderColor:'#343a40',
    '&:hover': {
        backgroundColor: 'black',
        borderColor:'black',
    },
}));

const ClearButton = styled(Button)(({ theme }) => ({
    color: theme.palette.getContrastText('#000000'),
    fontFamily: `Shadows Into Light, cursive`,
    backgroundColor: '#b71c1c',
    borderColor:'#b71c1c',
    '&:hover': {
        backgroundColor: '#951313',
        borderColor:'#951313',
    },
}));

const CustomTextField = styled(TextField)({
    '& label.Mui-root': {
        fontFamily: `Shadows Into Light, cursive`,
    },
    '& label.Mui-focused': {
        color: '#4D3636',
        // fontFamily: `Shadows Into Light, cursive`,
    },
    '& .MuiInput-underline:after': {
        borderBottomColor: '#4D3636',
    },
    '& .MuiOutlinedInput-root': {
        '& fieldset': {
            borderColor: '#4D3636',
        },
        '&:hover fieldset': {
            borderColor: '#4D3636',
            borderWidth:'2px',
        },
        '&.Mui-focused fieldset': {
            borderColor: '#4D3636',
        },
    },
});

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
        <Grid container spacing={{ xs: 1, sm:2, md: 3, lg: 3 }} justifyContent="space-evenly" alignItems="center" style={styles.form}>
            <Grid item xs={12} sm={12} md={12} lg={12}>
                <CustomTextField 
                    label="Enter your text..." 
                    id="message" 
                    name="message" 
                    size="small"
                    autoFocus
                    fullWidth
                />
            </Grid>
            
            <Grid item xs={12} sm={6} md={6} lg={6}>
                <ResultButton 
                    variant="outlined"
                    id="buttonResult"
                    name="buttonResult"
                    value="Result"
                    style={styles.buttonResult}
                    onClick={handleResult}
                    fullWidth
                >
                    Result
                </ResultButton>
            </Grid>

            <Grid item xs={12} sm={6} md={6} lg={6}>
                <ClearButton 
                    variant="outlined"
                    id="buttonClear" 
                    name="buttonClear" 
                    style={styles.buttonClear} 
                    onClick={handleClear}
                    fullWidth
                >
                    Clear
                </ClearButton>
            </Grid>
        </Grid>
    )
}