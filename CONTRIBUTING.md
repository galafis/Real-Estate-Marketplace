# Diretrizes de Contribuição

Bem-vindo(a) ao projeto Real Estate Marketplace! Agradecemos o seu interesse em contribuir.

Para garantir um processo de colaboração eficiente e harmonioso, por favor, siga as diretrizes abaixo:

## Como Contribuir

1.  **Faça um Fork do Repositório**: Comece fazendo um fork deste repositório para a sua conta GitHub.

2.  **Clone o Repositório Forkado**: Clone o seu fork para a sua máquina local:

    ```bash
    git clone https://github.com/SEU_USUARIO/real_estate_marketplace.git
    cd real_estate_marketplace
    ```

3.  **Crie uma Nova Branch**: Crie uma branch para a sua contribuição. Use um nome descritivo para a branch (ex: `feature/nova-funcionalidade`, `bugfix/correcao-erro-login`).

    ```bash
    git checkout -b feature/sua-feature
    ```

4.  **Faça Suas Alterações**: Implemente suas alterações ou novas funcionalidades. Certifique-se de que seu código siga os padrões de estilo do projeto e que todos os testes passem.

5.  **Teste Suas Alterações**: Antes de enviar, execute os testes existentes e, se aplicável, adicione novos testes para cobrir suas alterações.

    ```bash
    PYTHONPATH=$(pwd) pytest tests/
    ```

6.  **Faça Commit das Suas Alterações**: Escreva mensagens de commit claras e concisas. Use o formato `Tipo: Descrição` (ex: `feat: Adiciona funcionalidade de busca por cidade`).

    ```bash
    git commit -m "feat: Adiciona nova funcionalidade X"
    ```

7.  **Envie para o Seu Fork**: Envie suas alterações para o seu repositório forkado no GitHub.

    ```bash
    git push origin feature/sua-feature
    ```

8.  **Abra um Pull Request (PR)**: Vá para o repositório original no GitHub e abra um Pull Request da sua branch para a branch `main` (ou a branch de desenvolvimento apropriada). Descreva suas alterações detalhadamente no PR.

## Padrões de Código

*   **Python**: Siga o PEP 8 para estilo de código Python.
*   **JavaScript**: Use um estilo consistente, preferencialmente ESLint.
*   **HTML/CSS**: Mantenha o código limpo, semântico e responsivo.

## Relatando Bugs

Se você encontrar um bug, por favor, abra uma issue no GitHub. Inclua o máximo de detalhes possível:

*   Passos para reproduzir o bug.
*   Comportamento esperado.
*   Comportamento observado.
*   Capturas de tela (se aplicável).
*   Versão do sistema operacional, navegador, etc.

## Sugestões de Melhoria

Ideias para novas funcionalidades ou melhorias são sempre bem-vindas! Abra uma issue para discutir suas sugestões.

Obrigado(a) por contribuir para o Real Estate Marketplace!

