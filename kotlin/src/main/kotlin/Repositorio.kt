import org.springframework.jdbc.core.BeanPropertyRowMapper
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.jdbc.core.PreparedStatementCallback
import java.util.*
import javax.swing.JOptionPane
import javax.swing.JOptionPane.*

class Repositorio {

    var fkEmpresa:Int = 0
    var fkPlano:Int = 0
    var fkMaquina:Int = 0
    var fkTipoMaquina:Int = 0
    var fkLocal:Int = 0

    lateinit var jdbcTemplate: JdbcTemplate

    fun iniciar() {
        jdbcTemplate = Conexao.jdbcTemplate!!
    }

    fun validarColaborador() {

        val email = showInputDialog("Digite Seu Email:")
        val senha = showInputDialog("Digite Sua Senha:")

        // puxando o colaborador
        val loginQuery = "SELECT COUNT(*) FROM Colaborador WHERE email = ? AND senha = ?"
        val count = jdbcTemplate.execute(loginQuery, PreparedStatementCallback { preparedStatement ->
            preparedStatement.setString(1, email)
            preparedStatement.setString(2, senha)
            val resultSet = preparedStatement.executeQuery()
            resultSet.next()
            resultSet.getInt(1)
        })

        // validando se existe no banco
        if (count != null) {
            if (count > 0) {
                val nomeQuery = "SELECT nome FROM Colaborador WHERE email = ? AND senha = ?"
                val nome = jdbcTemplate.execute(nomeQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setString(1, email)
                    preparedStatement.setString(2, senha)
                    val nomeResultSet = preparedStatement.executeQuery()
                    nomeResultSet.next()
                    nomeResultSet.getString("nome")
                })

                // puxando a fkNivelAcesso
                val fkNivelAcessoQuery = "SELECT fkNivelAcesso FROM Colaborador WHERE email = ? AND senha = ?"
                val fkNivelAcesso = jdbcTemplate.execute(fkNivelAcessoQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setString(1, email)
                    preparedStatement.setString(2, senha)
                    val nivelAcessoResultSet = preparedStatement.executeQuery()
                    nivelAcessoResultSet.next()
                    nivelAcessoResultSet.getInt("fkNivelAcesso")
                })

                // arrumando o nivel de acesso
                val cargo = when (fkNivelAcesso) {
                    1 -> "Representante Legal"
                    2 -> "Gerente de TI"
                    3 -> "Equipe de TI"
                    else -> "Cargo desconhecido"
                }

                showMessageDialog(null, "Bem Vindo(a) $nome - Logado como: $cargo")

                // puxando a fkEmpresa
                val fkEmpresaQuery = "SELECT fkEmpresa FROM Colaborador WHERE email = ? AND senha = ?"
                fkEmpresa = jdbcTemplate.execute(fkEmpresaQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setString(1, email)
                    preparedStatement.setString(2, senha)
                    val resultSet = preparedStatement.executeQuery()
                    resultSet.next()
                    resultSet.getInt("fkEmpresa")
                })

                // puxando a fkPlano
                val fkPlanoQuery = "select fkPlano from Colaborador join Empresa on fkEmpresa = idEmpresa WHERE email = ? AND senha = ?"
                fkPlano = jdbcTemplate.execute(fkPlanoQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setString(1, email)
                    preparedStatement.setString(2, senha)
                    val resultSet = preparedStatement.executeQuery()
                    resultSet.next()
                    resultSet.getInt("fkPlano")
                })

                // mostrando as máquinas disponiveis
                val fkMaquinaQuery = "select idMaquina, SO, IP, sala, andar, nome from Maquina JOIN LocalSala on fkLocal = idLocalSala join setor on fkSetor = idSetor;"

                val maquinasDispo = jdbcTemplate.query(fkMaquinaQuery) { resultSet, _ ->
                    val idMaquina = resultSet.getInt("idMaquina")
                    val so = resultSet.getString("SO")
                    val ip = resultSet.getString("IP")
                    val sala = resultSet.getString("sala")
                    val andar = resultSet.getInt("andar")
                    val nome = resultSet.getString("nome")

                    println("ID: $idMaquina, SO: $so, IP: $ip, Sala: $sala, Andar: $andar, Setor: $nome")
                }

                println("Número de máquinas disponíveis: ${maquinasDispo.size}")

                // puxando a fkMaquina
                val maquinaOpcao = JOptionPane.showInputDialog("Escolha um ID:").toInt()
                fkMaquina = maquinaOpcao

                showMessageDialog(
                    null, """
                    Seu monitoramento está rodando
                           Verifique seu Banco!!!
                    """.trimIndent()
                )

                // puxando o fTipoMaquina
                val fkTipoMaquinaQuery = "select fkTipoMaquina from maquina WHERE idMaquina = ?"
                fkTipoMaquina = jdbcTemplate.execute(fkTipoMaquinaQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setInt(1, maquinaOpcao)
                    val resultSet = preparedStatement.executeQuery()
                    resultSet.next()
                    resultSet.getInt("fkTipoMaquina")
                })

                // puxando a fkLocal
                val fkLocalQuery = "select fkLocal from maquina WHERE idMaquina = ?"
                fkLocal = jdbcTemplate.execute(fkLocalQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setInt(1, maquinaOpcao)
                    val resultSet = preparedStatement.executeQuery()
                    resultSet.next()
                    resultSet.getInt("fkLocal")
                })

                println("Para finalizar seu monitoramento feche a aplicação.")

            } else {
                showMessageDialog(null, "Login Inválido")
            }
        }
    }
}