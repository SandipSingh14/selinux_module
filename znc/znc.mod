��|�   SE Linux Module                   znc   1.0@                                             chr_file      write      ioctl      getattr      read                    process
      transition                    file      write
      entrypoint      setattr      read                object_r@           @           @                   @                     unconfined_r@   @                 @   @                 @                   @                 	                @   @            `     file_type	                @   @                  exec_type
                @   @                  entry_type                @   @            @     user_home_content_type                @   @                 kernel_system_state_reader                @   @                 userdom_filetrans_type         	       @           znc_t                @   @                 corenet_unlabeled_type                @   @            `     non_security_file_type                @           user_devpts_t                @           urandom_device_t                @           random_device_t                @   @                 userdom_home_manager_type
                @   @            @     polymember
                @           znc_exec_t
                @           znc_home_t                @   @                  application_exec_type                @   @                 netlabel_peer_type                @   @            P     ubac_constrained_type                @   @            `     non_auth_file_type                @   @                 application_domain_type                @   @                 nsswitch_domain                @           unconfined_t                @   @            @     user_home_type   	             @   @                 kerberos_keytab_domain   
             @   @                 domain                                                           @   @                 @               @   @                  @                               @   @                 @               @   @                 @                               @   @                 @               @   @                  @                               @   @                 @               @   @                 @                               @   @                 @               @   @                 @                               @   @                 @               @   @                 @                               @   @                 @               @   @            �     @                               @   @                 @               @   @                  @                                        @           @   @                 @   @                 @   @          ���    @           @           @           @              @   @                 @   @                 @   @                 @           @           @           @   @            p     @           @           @           @                                                                                         chr_file            process            file               object_r            unconfined_r            	   file_type         	   exec_type         
   entry_type            user_home_content_type            kernel_system_state_reader            userdom_filetrans_type            znc_t            corenet_unlabeled_type            non_security_file_type            user_devpts_t            urandom_device_t            random_device_t            userdom_home_manager_type         
   polymember         
   znc_exec_t         
   znc_home_t            application_exec_type            netlabel_peer_type            ubac_constrained_type            non_auth_file_type            application_domain_type            nsswitch_domain            unconfined_t            user_home_type            kerberos_keytab_domain            domain                             