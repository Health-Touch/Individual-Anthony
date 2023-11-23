var database = require("../database/config");

function buscarUltimasMedidasCpu(idMaquina) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "cpu" and Monitoramento.fkMaquina = ${idMaquina};`;
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "cpu" and Monitoramento.fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarMedidasEmTempoRealCpu(idMaquina) {
console.log(idMaquina + "entrei")
    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "cpu" and Monitoramento.fkMaquina = ${idMaquina};`;
        

    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "cpu" and Monitoramento.fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return

    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarUltimasMedidasDisco(idMaquina) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "disco" and Monitoramento.fkMaquina = ${idMaquina};`;
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "disco" and Monitoramento.fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarMedidasEmTempoRealDisco(idMaquina) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "disco" and Monitoramento.fkMaquina = ${idMaquina};`;

    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "disco" and Monitoramento.fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarUltimasMedidasRam(ram) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "ram";`;
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "ram";`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarMedidasEmTempoRealRam(ram) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "ram";`;

    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select porcentagem, DATE_FORMAT(dataHora, '%Hh') AS horario from Monitoramento join Componente on idComponente = fkComponente where nome = "ram";`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

// começo do individual do tony
function buscarMedidasUpload(idMaquina) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select upload, DATE_FORMAT(dataHora, '%Hh:%i:%s') AS Horário from monitoramentoRede where fkMaquina = ${idMaquina};`;
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select upload, DATE_FORMAT(dataHora, '%Hh:%i:%s') AS Horário from monitoramentoRede where fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarMedidasDownload(idMaquina) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select download, DATE_FORMAT(dataHora, '%Hh:%i:%s') AS Horário from monitoramentoRede where fkMaquina = ${idMaquina};`;
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select download, DATE_FORMAT(dataHora, '%Hh:%i:%s') AS Horário from monitoramentoRede where fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarMedidasRede(idMaquina) {

    instrucaoSql = ''

    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select download, upload, DATE_FORMAT(dataHora, '%Hh:%i') AS Horário from monitoramentoRede where fkMaquina = ${idMaquina};`;
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select download, upload, DATE_FORMAT(dataHora, '%Hh:%i') AS Horário from monitoramentoRede where fkMaquina = ${idMaquina};`;
    } else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}


// fim do individual do tony

module.exports = {
    buscarUltimasMedidasCpu,
    buscarMedidasEmTempoRealCpu,
    buscarUltimasMedidasDisco,
    buscarMedidasEmTempoRealDisco,
    buscarUltimasMedidasRam,
    buscarMedidasEmTempoRealRam,
    buscarMedidasRede
}
