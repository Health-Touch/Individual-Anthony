import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.jdbc.core.PreparedStatementCallback
import javax.swing.JOptionPane.*

class Repositorio {

    lateinit var jdbcTemplate: JdbcTemplate

    fun iniciar() {
        jdbcTemplate = Conexao.jdbcTemplate!!
    }

    fun validarColaborador() {

        val email = showInputDialog("Digite Seu Email:")
        val senha = showInputDialog("Digite Sua Senha:")

        val loginQuery = "SELECT COUNT(*) FROM Colaborador WHERE email = ? AND senha = ?"
        val count = jdbcTemplate.execute(loginQuery, PreparedStatementCallback { preparedStatement ->
            preparedStatement.setString(1, email)
            preparedStatement.setString(2, senha)
            val resultSet = preparedStatement.executeQuery()
            resultSet.next()
            resultSet.getInt(1)
        })

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

                val fkNivelAcessoQuery = "SELECT fkNivelAcesso FROM Colaborador WHERE email = ? AND senha = ?"
                val fkNivelAcesso = jdbcTemplate.execute(fkNivelAcessoQuery, PreparedStatementCallback { preparedStatement ->
                    preparedStatement.setString(1, email)
                    preparedStatement.setString(2, senha)
                    val nivelAcessoResultSet = preparedStatement.executeQuery()
                    nivelAcessoResultSet.next()
                    nivelAcessoResultSet.getInt("fkNivelAcesso")
                })

                val cargo = when (fkNivelAcesso) {
                    1 -> "Representante Legal"
                    2 -> "Gerente de TI"
                    3 -> "Equipe de TI"
                    else -> "Cargo desconhecido"
                }

                showMessageDialog(null, "Bem Vindo(a) $nome - Logado como: $cargo")


            } else {
                showMessageDialog(null, "Login Inválido")
            }
        }
    }
}