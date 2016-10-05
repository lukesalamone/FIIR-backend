<?php
	// echo print_r($GLOBALS, true);
        if(count($_POST) !== 0){
                if($_POST['action'] === 'refresh'){
                        $price = 0;
                        switch($_POST['price']){
                                case "vip":
                                        $price = 1000;
                                        break;
                                case "wild":
                                        $price = 100;
                                        break;
                                case "fiir":
                                        $price = 1;
                                        break;
                                default:
                                        echo(json_encode(['status'=>'err','message'=>'malformed request']));
                                        return;
                        }
                        $after = intval($_POST['after']);
                        echo json_encode(getRecent($price, $after));
                }
                return;
        }
	
	// return array of metadata for most recent pics
        function getRecent($price, $after){
                $db = new PDO('mysql:host=localhost;dbname=fiir','root','1234qwerZ');
                $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

                $stmt = $db->prepare("select * from PICS where price = :price order by date_added desc limit 10");
                // $stmt = $db->prepare("select * from PICS");
		$stmt->bindValue(':price', $price);
                $stmt->execute();
                $result = $stmt->fetchAll();
		
		// echo print_r($result, true);

                $ret = array();

                for($i=0; $i<count($result); $i++){
                        $r = $result[$i];
                        $row = array(
                                'date'          =>      $r['date_added'],
                                'twitter'       =>      $r['twitter_URL'],
                                'instagram'     =>      $r['instagram_URL'],
                                'link'          =>      $r['filename'],
                                'tag1'          =>      $r['tag_1'],
                                'tag2'          =>      $r['tag_2'],
                                'tag3'          =>      $r['tag_3']
                        );
                        $ret[$i] = $row;
                }
                return $ret;
        }

?>

