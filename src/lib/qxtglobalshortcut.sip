%Module qxtglobalshortcut 0

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip

class QxtGlobalShortcut : QObject
{

%TypeHeaderCode
#include <qxtglobalshortcut.h>
%End

public:
    explicit QxtGlobalShortcut(QObject *parent /TransferThis/ = 0);
    explicit QxtGlobalShortcut(const QKeySequence& shortcut, QObject *parent /TransferThis/ = 0);
    virtual ~QxtGlobalShortcut();

    QKeySequence shortcut() const;
    bool setShortcut(const QKeySequence& shortcut);

    bool isEnabled() const;

public slots:
    void setEnabled(bool);
    void setDisabled(bool);

signals:
    void activated();
};
