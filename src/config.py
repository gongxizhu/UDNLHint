def GetConfigs(env='dev'):
    import config_dev
    configs = config_dev.configs
    if(env=='qa'):
        try:
            import config_qa
            configs = {**configs, **config_qa.configs}
        except ImportError:
            pass
    
    return configs

# configs = GetConfigs()
# print(configs['db']['host'])