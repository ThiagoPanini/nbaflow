"""
---------------------------------------------------
------------------- MÓDULO: s3 --------------------
---------------------------------------------------
Módulo responsável por alocar desenvolvimentos
relacionados à utilização do SDK Python boto3 para
o gerencimento do serviço s3 (Simple Storage Service)
da AWS. O objetivo deste arquivo é providenciar
funções, classes e métodos encapsulados capazes de
facilitar o desenvolvimento de aplicações que 
necessitem utilizar o serviço de s3 de armazenamento
de objetos na nuvem.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
2. Simple Storage Service
    2.1 Classe estruturada para operações no s3
    2.2 Funções de utilidade geral
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 27/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# SDK Python
import boto3
from botocore.exceptions import ClientError

# Bibliotecas padrão
import os

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
               1.2 Configurando logs
---------------------------------------------------
"""

# Definindo função para configurar objeto de log do código
def log_config(logger, level=logging.DEBUG, 
               log_format='%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s',
               log_filepath=os.path.join(os.getcwd(), 'exec_log/execution_log.log'),
               flag_file_handler=False, flag_stream_handler=True, filemode='a'):
    """
    Função que recebe um objeto logging e aplica configurações básicas ao mesmo
    
    Parâmetros
    ----------
    :param logger: objeto logger criado no escopo do módulo [type: logging.getLogger()]
    :param level: level do objeto logger criado [type: level, default=logging.DEBUG]
    :param log_format: formato do log a ser armazenado [type: string]
    :param log_filepath: caminho onde o arquivo .log será armazenado 
        [type: string, default='exec_log/execution_log.log']
    :param flag_file_handler: define se será criado um arquivo de armazenamento de log
        [type: bool, default=False]
    :param flag_stream_handler: define se as mensagens de log serão mostradas na tela
        [type: bool, default=True]
    :param filemode: tipo de escrita no arquivo de log [type: string, default='a' (append)]
    
    Retorno
    -------
    :return logger: objeto logger pré-configurado
    """

    # Setting level for the logger object
    logger.setLevel(level)

    # Creating a formatter
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Creating handlers
    if flag_file_handler:
        log_path = '/'.join(log_filepath.split('/')[:-1])
        if not os.path.isdir(log_path):
            os.makedirs(log_path)

        # Adding file_handler
        file_handler = logging.FileHandler(log_filepath, mode=filemode, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if flag_stream_handler:
        # Adding stream_handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)    
        logger.addHandler(stream_handler)

    return logger

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Definindo parâmetro de região para uso nas funções
REGION = 'sa-east-1'


"""
---------------------------------------------------
------------ 2. SIMPLE STORAGE SERVICE ------------
     2.1 Classe estruturada para operações no s3
---------------------------------------------------
"""

class JimmyBuckets():
    """
    Classe construída para facilitar a aplicação de operações
    básicas no s3 utilizando SDK Python boto3. Com ela, é 
    possível utilizar métodos encapsulados para operações de
    criação, exclusão, upload e leitura de objetos em buckets
    no s3. Cada instância de objeto desta classe recebe um 
    único argumento referente à região de atuação para que, 
    em seu método construtor, seja possível instanciar um
    recurso e um client s3 via boto3.

    Atributos da classe
    -------------------
    :attr region:
        Região de utilização dos recursos s3 da AWS. Por 
        padrão, o módulo contém uma variável atribuída
        no início do código que define uma região em
        específico que, ao mesmo tempo, pode ser modificada
        no ato de instância desta classe.
        [type: string, default='sa-east-1']
    """

    def __init__(self, region=REGION):
        # Instanciando recurso e client s3 via boto3
        self.region = region
        self.s3_resource = boto3.resource('s3', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)

    # Criando novos buckets na AWS
    def create_bucket(self, bucket_name, acl='private', **kwargs):
        """
        Método criado para consolidar os principais elementos de
        criação de buckets s3 através do SDK boto3. O código aqui
        encapsulado visa propor um detalhamento mais claro sobre
        as etapas mais comuns de criação de bucket, providenciando
        ao usuário uma maior abstração nas configurações mais
        básicas dentro deste universo. De maneira geral, esta
        função instancia um recurso s3 via boto3 e utiliza o método
        create_bucket() para consolidar as operações de criação
        de buckets.
        
        Para detalhes adicionais ou operações mais avançadas
        relacionadas à criação de buckets, verificar a documentação
        oficial do boto3 na AWS.
        
        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser criado dentro da conta
            AWS configurada para a utilização do boto3. O nome
            do bucket deve seguir as diretrizes propostas pela
            própria AWS dentro das boas práticas e restrições
            estabelecidas.
            [type: string]
            
        :param acl:
            Parâmetro que define o controle de acesso definido
            para o bucket (Access Control List). Neste contexto
            o argumento acl propõe a utilização de um bloco
            consolidado de controle predefinido dentro das 
            diretrizes da AWS. Através da documentação de 
            referência do SDK, é possível visualizar as opções 
            possíveis enblocadas para a definição de controle 
            de acesso.
            [type: string, default='private']
            
        Argumentos Adicionais
        ---------------------
        :kwarg block_public:
            Flag que define a modificação da política de acesso
            ao bucket criado. Ao ser configurado como True, é
            instanciado um client s3 via boto3 e executado o
            método put_public_access_block() para bloqueio de
            todo acesso público proveniente ACLs ou configurações
            adicionais do bucket. A definição exata do bloqueio
            de acesso público é definida a partir do argumento
            adicional block_public_config.
            [type: bool, default=True]
        
        :kwarg block_public_config:
            Dicionário de configuração com chaves específicas 
            de definição das restrições a serem aplicadas no
            método put_public_acess_block() do client s3
            instanciado.
            [type: dict, default={
                            'BlockPublicAcls': True,
                            'IgnorePublicAcls': True,
                            'BlockPublicPolicy': True,
                            'RestrictPublicBuckets': True
                        }]
        """

        # Criando um novo bucket
        try:
            location = kwargs['location'] if 'location' in kwargs else {'LocationConstraint': self.region}
            self.s3_resource.create_bucket(
                Bucket=bucket_name, 
                ACL=acl,
                CreateBucketConfiguration=location
            )
            logger.info(f'Bucket {bucket_name} criado com sucesso.')

        except (self.s3_client.exceptions.BucketAlreadyExists, self.s3_client.exceptions.BucketAlreadyOwnedByYou) as e:
            logger.warning(f'Bucket {bucket_name} já existente. A criação de um novo bucket não será realizada. Exception: {e}')
            return None

        except ClientError as ce:
            logger.error(f'Erro durante a criação do bucket. Exception: {ce}')
                
        # Validando bloqueio de acesso público ao bucket
        block_public = kwargs['block_public'] if 'block_public' in kwargs else True
        if block_public:
            config = {
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
            block_public_config = kwargs['block_public_config'] if 'block_public_config' in kwargs else config
            
            # Instanciando sessão e configurando bloqueio de acesso público
            try:
                self.s3_client.put_public_access_block(Bucket=bucket_name,
                                                PublicAccessBlockConfiguration=block_public_config)
            except Exception as e:
                logger.warning(f'Erro ao instanciar client e bloquear acesso público ao bucket {bucket_name}. Exception: {e}')
                
    # Eliminando buckets já existentes na AWS
    def delete_bucket(self, bucket_name, empty_bucket=False):
        """
        Método criado para encapsular as ações relacionadas à 
        exclusão de buckets s3 através do SDK boto3. De maneira 
        geral, o método utiliza um recurso do s3 instanciado via 
        boto3 para a criação de um objeto "bucket" gerado através 
        do método resource.Bucket(), permitindo a posterior execução
        do método bucket.delete(). Em linha com as funcionalidades 
        deste módulo, este método comporta as principais tratativas 
        de erros encontradas no processo de exclusão de buckets, 
        permitindo assim um detalhamento claro e direto ao usuário. 
        
        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser criado dentro da conta
            AWS configurada para a utilização do boto3. O nome
            do bucket deve seguir as diretrizes propostas pela
            própria AWS dentro das boas práticas e restrições
            estabelecidas.
            [type: string]

        :param empty_bucket:
            Flag que define o esvaziamento do bucket, ou seja,
            a exclusão de todos os objetos existentes no mesmo.
            O gerenciamento incorreto deste argumento pode
            causar danos irreversíveis ao conteúdo do bucket
            selecionado e, portanto, sua atribuição deve ser
            realizada com cautela. No código, ao tentar eliminar 
            um bucket através do método bucket.delete(), a
            exceção ClientError é invocada e, por ela, a 
            verificação de esvaziamento de bucket é verificada
            para que todos os objetos sejam eliminados antes de
            uma nova tentativa de delete do bucket. Caso o código
            caia nesta exceção e o parâmetro empty_bucket esteja
            configurado como "False", a exclusão do bucket não
            é realizada.
            [type: bool, default=False]
        """

        # Deletando bucket 
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            bucket.delete()
            logger.info(f'Bucket {bucket_name} deletado com sucesso')
        
        except self.s3_client.exceptions.NoSuchBucket as nsbe:
            logger.warning(f'Bucket {bucket_name} inexistente. Nenhuma ação de delete realizada. Exception: {nsbe}')
            return None

        except ClientError as ce:
            # Coletando objetos do bucket e verificando flag de esvaziamento
            bucket_objects = [obj for obj in bucket.objects.all()]
            if len(bucket_objects) > 0 and empty_bucket:            
                # Esvaziando e deletando bucket
                logger.warning(f'O bucket {bucket_name} possui {len(bucket_objects)} objetos. Esvaziando bucket e tentando delete novamente.')
                try:
                    bucket.objects.all().delete()
                    bucket.delete()
                    logger.info(f'Bucket {bucket_name} deletado com sucesso.')
                except Exception as e:
                    logger.error(f'Erro ao esvaziar e deletar bucket {bucket_name}. Exception: {e}')
            else:
                # Bucket não está vazio e flag de esvaziamento não configurado
                logger.error(f'Erro ao deletar bucket {bucket_name}. O bucket possui {len(bucket_objects)} e o parâmetro "empty_bucket" é igual a False. Exception: {ce}')
            
    # Realizando upload de arquivos para buckets s3
    def upload_object(self, file, bucket_name, key, 
                      method='put_object', verbose=True):
        
        """
        Método criado para encapsular as ações relacionadas ao 
        upload de objetos em um bucket s3 utilizando o SDK boto3.
        Entre as possibilidades existentes, o usuário pode escolher,
        através do argumento "method" da função, realizar o upload 
        por dois diferentes métodos de um client: put_object() ou 
        upload_file().

        Com o method igual a put_object(), o usuário pode fornecer, para
        o argumento "file" deste método, um caminho de armazenamento
        local do objeto ou então o conteúdo binário do mesmo lido
        previamente no código. Já com o método upload_file(), o
        usuário deve passar obrigatoriamente apenas um caminho
        de armazenamento local do objeto.
        
        Parâmetros
        ----------
        :param file:
            Buffer binário do objeto alvo ou então string de
            referência de armazenamento local do arquivo (caso
            o método seja definido como upload_object()).
            [type: string or buffer]

        :param bucket_name:
            Referência do bucket a ser criado dentro da conta
            AWS configurada para a utilização do boto3. O nome
            do bucket deve seguir as diretrizes propostas pela
            própria AWS dentro das boas práticas e restrições
            estabelecidas.
            [type: string]
            
        :param key:
            Chave de armazenamento do objeto no s3.
            [type: string]

        :param method:
            Método de upload do objeto no bucket de referência.
            O usuário deve selecionar entre "put_object" ou
            "upload_file" para que, internamente, o método possa
            realizar a execução de um dos dois métodos do client
            instanciado. Como precaução, o usuário deve apenas
            atentar-se ao fato de que, caso o método escolhido
            seja "upload_file", o parâmetro "file" da função
            deve, obrigatoriamente, referenciar um caminho
            local de armazenamento do arquivo a ser ingerido.
            Adicionalmente, o método trata qualquer outro caso
            de possível equívoco caso o usuário selecione um
            método diferente dessas duas possibilidades, retornando
            uma mensagem e cancelando o processo de upload.
            [type: string, default="put_object"]

        :param verbose:
            Flag de verbosidade para logs aplicados durante
            as tratativas de upload de objetos no método.
            [type: bool, default=True]
        """

        # Verificando método de upload
        if method == 'put_object':
            # Realizando upload de stream binária já em buffer
            try:
                self.s3_client.put_object(Bucket=bucket_name, Body=file, Key=key)
            except Exception as e:
                logger.error(f'Erro ao realizar upload via client.put_object(). Exception: {e}')
                return None
        
        elif method == 'upload_file':
            # Realizando upload a partir de arquivo local
            try:
                self.s3_client.upload_file(Bucket=bucket_name, Filename=file, Key=key)
            except ValueError as ve:
                logger.error(f'Erro ao realizar upload via client.upload_file(). Exception: {ve}')
                return None
        
        else:
            logger.error(f'Método de upload "{method}" inválido. Selecione entre "put_object" ou "upload_file"')
            return None

        # Comunicando resultado
        if verbose:
            logger.info(f'Upload do objeto {key} realizado com sucesso no bucket {bucket_name}')

    # Realizando upload de todos os arquivos em um diretório local
    def upload_files_in_dir(self, directory, bucket_name, folder_prefix='',
                            method='put_object', inner_verbose=False, outer_verbose=True):
        """
        Método criado para com o objetivo de encapsular múltiplas
        execuções de upload de objetos no s3 presentes em um
        diretório local de referência. Em outras palavras, o
        argumento principal deste método é uma referência de 
        diretório que, por sua vez, será utilizada para verificar
        todos os subdiretórios e arquivos presentes, propondo assim
        múltiplas execuções da função upload_object() presente
        neste módulo.

        Visando propor uma melhor organização dos objetos a serem
        ingeridos no bucket, o método conta com uma lógica que
        coleta os subdiretórios encontrados e os transforma em
        prefixos (ou pastas) no s3, fazendo assim com que a mesma
        estrutura organizacional dos arquivos no dirtório raíz
        seja mantida também no s3.
        
        Parâmetros
        ----------
        :param directory:
            Referência local de diretório a ser utilizado como
            alvo de navegação para extração de todos os arquivos
            presentes. Na prática, a função utiliza o método
            os.walk() para coletar todos os subdiretórios e 
            arquivos do diretório em um laço de repetição que,
            ao final, chama a função de upload individual de
            objeto para cada referência de arquivo encontrada.
            [type: string]

        :param bucket_name:
            Referência do bucket a ser criado dentro da conta
            AWS configurada para a utilização do boto3. O nome
            do bucket deve seguir as diretrizes propostas pela
            própria AWS dentro das boas práticas e restrições
            estabelecidas.
            [type: string]

        :param folder_prefix:
            Propondo uma maior liberdade em definições de
            organização da estrutura a ser espelhada no bucket
            este argumento permite com que o usuário defina um
            prefixo (ou diretório) raíz a ser inserido no s3.
            Por padrão, o argumento contempla uma string vazia
            para que a mesma estrutura do diretório raíz seja
            espelhada no s3.
            [type: string, default='']
    
        :param method:
            Método de upload do objeto no bucket de referência.
            O usuário deve selecionar entre "put_object" ou
            "upload_file" para que, internamente, o método possa
            realizar a execução de um dos dois métodos do client
            instanciado. Como precaução, o usuário deve apenas
            atentar-se ao fato de que, caso o método escolhido
            seja "upload_file", o parâmetro "file" da função
            deve, obrigatoriamente, referenciar um caminho
            local de armazenamento do arquivo a ser ingerido.
            Adicionalmente, o método trata qualquer outro caso
            de possível equívoco caso o usuário selecione um
            método diferente dessas duas possibilidades, retornando
            uma mensagem e cancelando o processo de upload.
            [type: string, default="put_object"]

        :param key:
            Chave de armazenamento do objeto no s3.
            [type: string]

        :param inner_verbose:
            Flag de verbosidade para as mensagens de logs 
            aplicadas no método individual de upload de objetos. 
            Este parâmetro é passado para o parâmetro "verbose" 
            do método upload_object().
            [type: bool, default=False]

        :param outer_verbose:
            Flag de verbosidade para as mensagens de logs 
            aplicadas em laços externos neste método.
            [type: bool, default=True]
        """

        # Levantando parâmetros
        if outer_verbose:
            total_objects = len([name for _, _, files in os.walk(directory) for name in files])
            logger.debug(f'Iniciando upload para os {total_objects} objetos encontrados no diretório alvo')

        # Navegando por todos os arquivos em um diretório
        for path, dirs, files in os.walk(directory):
            for name in files:
                filepath = os.path.join(path, name)
                key = filepath.replace(directory, folder_prefix).replace(os.path.sep, '/')[1:]
                # Realizando ingestão de cada objeto encontrado
                upload_object(
                    file=filepath,
                    bucket_name=bucket_name,
                    key=key,
                    method=method,
                    verbose=inner_verbose
                )

        if outer_verbose:
            logger.info(f'Fim do processo de upload dos objetos encontrados no diretório')
    

"""
---------------------------------------------------
------------ 2. SIMPLE STORAGE SERVICE ------------
          2.2 Funções de utilidade geral
---------------------------------------------------
"""

# Criando novos buckets na AWS
def create_bucket(bucket_name, region=REGION, acl='private', 
                  s3_resource=None, s3_client=None, **kwargs):
    """
    Função criada para consolidar os principais elementos de
    criação de buckets s3 através do SDK boto3. O código aqui
    encapsulado visa propor um detalhamento mais claro sobre
    as etapas mais comuns de criação de bucket, providenciando
    ao usuário uma maior abstração nas configurações mais
    básicas dentro deste universo. De maneira geral, esta
    função instancia um recurso s3 via boto3 e utiliza o método
    create_bucket() para consolidar as operações de criação
    de buckets.
    
    Para detalhes adicionais ou operações mais avançadas
    relacionadas à criação de buckets, verificar a documentação
    oficial do boto3 na AWS.
    
    Parâmetros
    ----------
    :param bucket_name:
        Referência do bucket a ser criado dentro da conta
        AWS configurada para a utilização do boto3. O nome
        do bucket deve seguir as diretrizes propostas pela
        própria AWS dentro das boas práticas e restrições
        estabelecidas.
        [type: string]
        
    :param region:
        Região a qual o bucket será criado. Este argumento
        também é utilizado para a criação do dicionário
        de configuração de localização do bucket a ser 
        passado também como parâmetro do método
        create_bucket() do recurso s3 instanciado.
        [type: string, default='sa-east-1']
        
    :param acl:
        Parâmetro que define o controle de acesso definido
        para o bucket (Access Control List). Neste contexto
        o argumento acl propõe a utilização de um bloco
        consolidado de controle predefinido dentro das 
        diretrizes da AWS. Através da documentação de 
        referência do SDK, é possível visualizar as opções 
        possíveis enblocadas para a definição de controle 
        de acesso.
        [type: string, default='private']
        
    Argumentos Adicionais
    ---------------------
    :kwarg block_public:
        Flag que define a modificação da política de acesso
        ao bucket criado. Ao ser configurado como True, é
        instanciado um client s3 via boto3 e executado o
        método put_public_access_block() para bloqueio de
        todo acesso público proveniente ACLs ou configurações
        adicionais do bucket. A definição exata do bloqueio
        de acesso público é definida a partir do argumento
        adicional block_public_config.
        [type: bool, default=True]
    
    :kwarg block_public_config:
        Dicionário de configuração com chaves específicas 
        de definição das restrições a serem aplicadas no
        método put_public_acess_block() do client s3
        instanciado.
        [type: dict, default={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }]
    """
    
    # Instanciando recurso e client S3
    if s3_resource is None:
        s3_resource = boto3.resource('s3', region_name=region)
    if s3_client is None:
        s3_client = boto3.client('s3', region_name=region)

    # Criando um novo bucket
    try:
        location = kwargs['location'] if 'location' in kwargs else {'LocationConstraint': region}
        s3_resource.create_bucket(
            Bucket=bucket_name, 
            ACL=acl,
            CreateBucketConfiguration=location
        )
        logger.info(f'Bucket {bucket_name} criado com sucesso.')

    except (s3_client.exceptions.BucketAlreadyExists, s3_client.exceptions.BucketAlreadyOwnedByYou) as e:
        logger.warning(f'Bucket {bucket_name} já existente. A criação de um novo bucket não será realizada. Exception: {e}')
        return None

    except ClientError as ce:
        logger.error(f'Erro durante a criação do bucket. Exception: {ce}')
            
    # Validando bloqueio de acesso público ao bucket
    block_public = kwargs['block_public'] if 'block_public' in kwargs else True
    if block_public:
        config = {
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
        block_public_config = kwargs['block_public_config'] if 'block_public_config' in kwargs else config
        
        # Instanciando sessão e configurando bloqueio de acesso público
        try:
            s3_client.put_public_access_block(Bucket=bucket_name,
                                              PublicAccessBlockConfiguration=block_public_config)
        except Exception as e:
            logger.warning(f'Erro ao instanciar client e bloquear acesso público ao bucket {bucket_name}. Exception: {e}')
            
# Eliminando buckets já existentes na AWS
def delete_bucket(bucket_name, region=REGION, empty_bucket=False, 
                  s3_resource=None, **kwargs):
    """
    Função criada para encapsular as ações relacionadas à 
    exclusão de buckets s3 através do SDK boto3. De maneira 
    geral, a função utiliza um recurso do s3 instanciado via 
    boto3 para a criação de um objeto "bucket" gerado através 
    do método resource.Bucket(), permitindo a posterior execução
    do método bucket.delete(). Em linha com as funcionalidades 
    deste módulo, a função comporta as principais tratativas 
    de erros encontradas no processo de exclusão de buckets, 
    permitindo assim um detalhamento claro e direto ao usuário. 
    
    Adicionalmente, a função possui um argumento s3_resource 
    que permite ao usuário passar um recurso instanciado
    externamente para ser usado nos processos associados. 
    Caso este argumento permaneça como "None", o recurso s3
    é instanciado como uma etapa interna da função.
    
    Parâmetros
    ----------
    :param bucket_name:
        Referência do bucket a ser criado dentro da conta
        AWS configurada para a utilização do boto3. O nome
        do bucket deve seguir as diretrizes propostas pela
        própria AWS dentro das boas práticas e restrições
        estabelecidas.
        [type: string]
        
    :param region:
        Região a qual o bucket será criado. Este argumento
        também é utilizado para a criação do dicionário
        de configuração de localização do bucket a ser 
        passado também como parâmetro do método
        create_bucket() do recurso s3 instanciado.
        [type: string, default='sa-east-1']

    :param empty_bucket:
        Flag que define o esvaziamento do bucket, ou seja,
        a exclusão de todos os objetos existentes no mesmo.
        O gerenciamento incorreto deste argumento pode
        causar danos irreversíveis ao conteúdo do bucket
        selecionado e, portanto, sua atribuição deve ser
        realizada com cautela. No código, ao tentar eliminar 
        um bucket através do método bucket.delete(), a
        exceção ClientError é invocada e, por ela, a 
        verificação de esvaziamento de bucket é verificada
        para que todos os objetos sejam eliminados antes de
        uma nova tentativa de delete do bucket. Caso o código
        caia nesta exceção e o parâmetro empty_bucket esteja
        configurado como "False", a exclusão do bucket não
        é realizada.
        [type: bool, default=False]
    """
    
    # Instanciando recurso S3 e listando buckets existentes
    if s3_resource is None:
        s3_resource = boto3.resource('s3', region_name=region)

    # Deletando bucket 
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.delete()
        logger.info(f'Bucket {bucket_name} deletado com sucesso')
    
    except boto3.client('s3').exceptions.NoSuchBucket as nsbe:
        logger.warning(f'Bucket {bucket_name} inexistente. Nenhuma ação de delete realizada. Exception: {nsbe}')
        return None

    except ClientError as ce:
        # Coletando objetos do bucket e verificando flag de esvaziamento
        bucket_objects = [obj for obj in bucket.objects.all()]
        if len(bucket_objects) > 0 and empty_bucket:            
            # Esvaziando e deletando bucket
            logger.warning(f'O bucket {bucket_name} possui {len(bucket_objects)} objetos. Esvaziando bucket e tentando delete novamente.')
            try:
                bucket.objects.all().delete()
                bucket.delete()
                logger.info(f'Bucket {bucket_name} deletado com sucesso.')
            except Exception as e:
                logger.error(f'Erro ao esvaziar e deletar bucket {bucket_name}. Exception: {e}')
        else:
            # Bucket não está vazio e flag de esvaziamento não configurado
            logger.error(f'Erro ao deletar bucket {bucket_name}. O bucket possui {len(bucket_objects)} e o parâmetro "empty_bucket" é igual a False. Exception: {ce}')
        
# Realizando upload de arquivos para buckets s3
def upload_object(file, bucket_name, key, region=REGION, 
                  method='put_object', s3_client=None, verbose=True):
    
    """
    Função criada para encapsular as ações relacionadas ao 
    upload de objetos em um bucket s3 utilizando o SDK boto3.
    Entre as possibilidades existentes, o usuário pode escolher,
    através do argumento "method" da função, realizar o upload 
    por dois diferentes métodos de um client: put_object() ou 
    upload_file().

    Com o método put_object(), o usuário pode fornecer, para
    o argumento "file" da função, um caminho de armazenamento
    local do objeto ou então o conteúdo binário do mesmo lido
    previamente no código. Já com o método upload_file(), o
    usuário deve passar obrigatoriamente apenas um caminho
    de armazenamento local do objeto.
    
    Adicionalmente, a função possui um argumento s3_client 
    que permite ao usuário passar um client instanciado
    externamente para ser usado nos processos associados. 
    Caso este argumento permaneça como "None", o client s3
    é instanciado como uma etapa interna da função.
    
    Parâmetros
    ----------
    :param file:
        Buffer binário do objeto alvo ou então string de
        referência de armazenamento local do arquivo (caso
        o método seja definido como upload_object()).
        [type: string or buffer]

    :param bucket_name:
        Referência do bucket a ser criado dentro da conta
        AWS configurada para a utilização do boto3. O nome
        do bucket deve seguir as diretrizes propostas pela
        própria AWS dentro das boas práticas e restrições
        estabelecidas.
        [type: string]
        
    :param region:
        Região a qual o bucket será criado. Este argumento
        também é utilizado para a criação do dicionário
        de configuração de localização do bucket a ser 
        passado também como parâmetro do método
        create_bucket() do recurso s3 instanciado.
        [type: string, default='sa-east-1']

    :param method:
        Método de upload do objeto no bucket de referência.
        O usuário deve selecionar entre "put_object" ou
        "upload_file" para que, internamente, a função possa
        realizar a execução de um dos dois métodos do client
        instanciado. Como precaução, o usuário deve apenas
        atentar-se ao fato de que, caso o método escolhido
        seja "upload_file", o parâmetro "file" da função
        deve, obrigatoriamente, referenciar um caminho
        local de armazenamento do arquivo a ser ingerido.
        Adicionalmente, a função trata qualquer outro caso
        de possível equívoco caso o usuário selecione um
        método diferente dessas duas possibilidades, retornando
        uma mensagem e cancelando o processo de upload.
        [type: string, default="put_object"]

    :param verbose:
        Flag de verbosidade para logs aplicados durante
        as tratativas de upload de objetos na função.
        [type: bool, default=True]
    """
    
    # Instanciando client S3
    if s3_client is None:
        s3_client = boto3.client('s3', region_name=region)

    # Verificando método de upload
    if method == 'put_object':
        # Realizando upload de stream binária já em buffer
        try:
            s3_client.put_object(Bucket=bucket_name, Body=file, Key=key)
        except Exception as e:
            logger.error(f'Erro ao realizar upload via client.put_object(). Exception: {e}')
            return None
    
    elif method == 'upload_file':
        # Realizando upload a partir de arquivo local
        try:
            s3_client.upload_file(Bucket=bucket_name, Filename=file, Key=key)
        except ValueError as ve:
            logger.error(f'Erro ao realizar upload via client.upload_file(). Exception: {ve}')
            return None
    
    else:
        logger.error(f'Método de upload "{method}" inválido. Selecione entre "put_object" ou "upload_file"')
        return None

    # Comunicando resultado
    if verbose:
        logger.info(f'Upload do objeto {key} realizado com sucesso no bucket {bucket_name}')

# Realizando upload de todos os arquivos em um diretório local
def upload_files_in_dir(directory, bucket_name, folder_prefix='',
                        region=REGION, method='put_object', s3_client=None,
                        inner_verbose=False, outer_verbose=True):
    """
    Função criada para com o objetivo de encapsular mútliplas
    execuções de upload de objetos no s3 presentes em um
    diretório local de referência. Em outras palavras, o
    argumento principal desta função é uma referência de 
    diretório que, por sua vez, será utilizada para verificar
    todos os subdiretórios e arquivos presentes, propondo assim
    múltiplas execuções da função upload_object() presente
    neste módulo.

    Visando propor uma melhor organização dos objetos a serem
    ingeridos no bucket, a função conta com uma lógica que
    coleta os subdiretórios encontrados e os transforma em
    prefixos (ou pastas) no s3, fazendo assim com que a mesma
    estrutura organizacional dos arquivos no dirtório raíz
    seja mantida também no s3.
    
    Adicionalmente, a função possui um argumento s3_client 
    que permite ao usuário passar um client instanciado
    externamente para ser usado nos processos associados. 
    Caso este argumento permaneça como "None", o client s3
    é instanciado como uma etapa interna da função.
    
    Parâmetros
    ----------
    :param directory:
        Referência local de diretório a ser utilizado como
        alvo de navegação para extração de todos os arquivos
        presentes. Na prática, a função utiliza o método
        os.walk() para coletar todos os subdiretórios e 
        arquivos do diretório em um laço de repetição que,
        ao final, chama a função de upload individual de
        objeto para cada referência de arquivo encontrada.
        [type: string]

    :param bucket_name:
        Referência do bucket a ser criado dentro da conta
        AWS configurada para a utilização do boto3. O nome
        do bucket deve seguir as diretrizes propostas pela
        própria AWS dentro das boas práticas e restrições
        estabelecidas.
        [type: string]

    :param folder_prefix:
        Propondo uma maior liberdade em definições de
        organização da estrutura a ser espelhada no bucket
        este argumento permite com que o usuário defina um
        prefixo (ou diretório) raíz a ser inserido no s3.
        Por padrão, o argumento contempla uma string vazia
        para que a mesma estrutura do diretório raíz seja
        espelhada no s3.
        [type: string, default='']
        
    :param region:
        Região a qual o bucket será criado. Este argumento
        também é utilizado para a criação do dicionário
        de configuração de localização do bucket a ser 
        passado também como parâmetro do método
        create_bucket() do recurso s3 instanciado.
        [type: string, default='sa-east-1']

    :param method:
        Método de upload do objeto no bucket de referência.
        O usuário deve selecionar entre "put_object" ou
        "upload_file" para que, internamente, a função possa
        realizar a execução de um dos dois métodos do client
        instanciado. Como precaução, o usuário deve apenas
        atentar-se ao fato de que, caso o método escolhido
        seja "upload_file", o parâmetro "file" da função
        deve, obrigatoriamente, referenciar um caminho
        local de armazenamento do arquivo a ser ingerido.
        Adicionalmente, a função trata qualquer outro caso
        de possível equívoco caso o usuário selecione um
        método diferente dessas duas possibilidades, retornando
        uma mensagem e cancelando o processo de upload.
        [type: string, default="put_object"]

    :param inner_verbose:
        Flag de verbosidade para as mensagens de logs 
        aplicadas no método individual de upload de objetos. 
        Este parâmetro é passado para o parâmetro "verbose" 
        da função upload_object().
        [type: bool, default=False]

    :param outer_verbose:
        Flag de verbosidade para as mensagens de logs 
        aplicadas em laços externos nesta função.
        [type: bool, default=True]
    """

    # Levantando parâmetros
    if outer_verbose:
        total_objects = len([name for _, _, files in os.walk(directory) for name in files])
        logger.debug(f'Iniciando upload para os {total_objects} objetos encontrados no diretório alvo')

    # Navegando por todos os arquivos em um diretório
    for path, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(path, name)
            key = filepath.replace(directory, folder_prefix).replace(os.path.sep, '/')[1:]
            # Realizando ingestão de cada objeto encontrado
            upload_object(
                file=filepath,
                bucket_name=bucket_name,
                key=key,
                region=region,
                method=method,
                s3_client=s3_client,
                verbose=inner_verbose
            )

    if outer_verbose:
        logger.info(f'Fim do processo de upload dos objetos encontrados no diretório')

